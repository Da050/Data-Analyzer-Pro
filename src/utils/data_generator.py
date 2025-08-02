"""
Utility functions for data generation and preprocessing.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_sample_data(filename='data/sample_data.csv', n_samples=1000):
    """
    Generate sample dataset for demonstration purposes.
    
    Args:
        filename: output filename
        n_samples: number of samples to generate
    """
    # Ensure data directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate synthetic data
    data = {
        'age': np.random.normal(35, 12, n_samples).astype(int),
        'income': np.random.lognormal(10.5, 0.5, n_samples),
        'education_years': np.random.normal(14, 3, n_samples),
        'experience_years': np.random.exponential(8, n_samples),
        'satisfaction_score': np.random.beta(2, 1, n_samples) * 10,
        'department': np.random.choice(['Engineering', 'Sales', 'Marketing', 'HR', 'Finance'], n_samples),
        'city': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'], n_samples),
        'performance_rating': np.random.choice([1, 2, 3, 4, 5], n_samples, p=[0.05, 0.15, 0.4, 0.3, 0.1])
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add some correlations and realistic constraints
    df['age'] = np.clip(df['age'], 18, 65)
    df['education_years'] = np.clip(df['education_years'], 8, 22).astype(int)
    df['experience_years'] = np.clip(df['experience_years'], 0, df['age'] - 18).astype(int)
    
    # Income correlated with education and experience
    df['income'] = df['income'] * (1 + 0.1 * df['education_years']) * (1 + 0.05 * df['experience_years'])
    df['income'] = np.round(df['income'], 2)
    
    # Satisfaction correlated with income and performance
    df['satisfaction_score'] = df['satisfaction_score'] + 0.3 * df['performance_rating'] + np.log(df['income']) * 0.1
    df['satisfaction_score'] = np.clip(df['satisfaction_score'], 0, 10)
    df['satisfaction_score'] = np.round(df['satisfaction_score'], 1)
    
    # Add some missing values randomly
    missing_indices = np.random.choice(df.index, size=int(0.05 * len(df)), replace=False)
    df.loc[missing_indices, 'satisfaction_score'] = np.nan
    
    # Add date column
    start_date = datetime(2020, 1, 1)
    df['hire_date'] = [start_date + timedelta(days=int(x)) for x in 
                      np.random.randint(0, 1400, n_samples)]
    
    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"✅ Sample data generated: {filename}")
    print(f"   Shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")
    
    return df

def clean_data(data, strategy='mean'):
    """
    Clean and preprocess data.
    
    Args:
        data: pandas DataFrame
        strategy: 'mean', 'median', 'drop' for handling missing values
    """
    cleaned_data = data.copy()
    
    # Handle missing values
    if strategy == 'mean':
        numeric_columns = cleaned_data.select_dtypes(include=[np.number]).columns
        cleaned_data[numeric_columns] = cleaned_data[numeric_columns].fillna(
            cleaned_data[numeric_columns].mean()
        )
    elif strategy == 'median':
        numeric_columns = cleaned_data.select_dtypes(include=[np.number]).columns
        cleaned_data[numeric_columns] = cleaned_data[numeric_columns].fillna(
            cleaned_data[numeric_columns].median()
        )
    elif strategy == 'drop':
        cleaned_data = cleaned_data.dropna()
    
    # Fill categorical missing values with mode
    categorical_columns = cleaned_data.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        if cleaned_data[col].isnull().sum() > 0:
            cleaned_data[col] = cleaned_data[col].fillna(cleaned_data[col].mode()[0])
    
    return cleaned_data

def encode_categorical_variables(data, columns=None, method='label'):
    """
    Encode categorical variables.
    
    Args:
        data: pandas DataFrame
        columns: list of columns to encode (if None, encode all categorical)
        method: 'label' or 'onehot'
    """
    encoded_data = data.copy()
    
    if columns is None:
        columns = data.select_dtypes(include=['object']).columns
    
    if method == 'label':
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        for col in columns:
            if col in data.columns:
                encoded_data[col] = le.fit_transform(data[col].astype(str))
    
    elif method == 'onehot':
        encoded_data = pd.get_dummies(encoded_data, columns=columns, prefix=columns)
    
    return encoded_data

def detect_and_handle_outliers(data, columns=None, method='iqr', action='cap'):
    """
    Detect and handle outliers.
    
    Args:
        data: pandas DataFrame
        columns: list of columns to check (if None, check all numeric)
        method: 'iqr' or 'zscore'
        action: 'cap', 'remove', or 'flag'
    """
    processed_data = data.copy()
    
    if columns is None:
        columns = data.select_dtypes(include=[np.number]).columns
    
    outlier_info = {}
    
    for col in columns:
        if method == 'iqr':
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = (data[col] < lower_bound) | (data[col] > upper_bound)
        
        elif method == 'zscore':
            from scipy import stats
            z_scores = np.abs(stats.zscore(data[col].dropna()))
            outliers = z_scores > 3
        
        outlier_count = outliers.sum()
        outlier_info[col] = outlier_count
        
        if action == 'cap' and method == 'iqr':
            processed_data[col] = np.clip(processed_data[col], lower_bound, upper_bound)
        elif action == 'remove':
            processed_data = processed_data[~outliers]
        elif action == 'flag':
            processed_data[f'{col}_outlier'] = outliers
    
    print("Outlier Detection Summary:")
    for col, count in outlier_info.items():
        print(f"  {col}: {count} outliers detected")
    
    return processed_data, outlier_info

def create_time_features(data, date_column):
    """
    Create time-based features from a date column.
    
    Args:
        data: pandas DataFrame
        date_column: name of the date column
    """
    enhanced_data = data.copy()
    
    # Convert to datetime if not already
    enhanced_data[date_column] = pd.to_datetime(enhanced_data[date_column])
    
    # Extract time features
    enhanced_data[f'{date_column}_year'] = enhanced_data[date_column].dt.year
    enhanced_data[f'{date_column}_month'] = enhanced_data[date_column].dt.month
    enhanced_data[f'{date_column}_day'] = enhanced_data[date_column].dt.day
    enhanced_data[f'{date_column}_dayofweek'] = enhanced_data[date_column].dt.dayofweek
    enhanced_data[f'{date_column}_quarter'] = enhanced_data[date_column].dt.quarter
    enhanced_data[f'{date_column}_is_weekend'] = enhanced_data[date_column].dt.dayofweek >= 5
    
    return enhanced_data

def split_data_by_time(data, date_column, split_date=None, train_ratio=0.8):
    """
    Split data based on time for time series analysis.
    
    Args:
        data: pandas DataFrame
        date_column: name of the date column
        split_date: specific date to split on (if None, use ratio)
        train_ratio: ratio for training data if split_date is None
    """
    # Sort by date
    sorted_data = data.sort_values(date_column)
    
    if split_date:
        train_data = sorted_data[sorted_data[date_column] < split_date]
        test_data = sorted_data[sorted_data[date_column] >= split_date]
    else:
        split_index = int(len(sorted_data) * train_ratio)
        train_data = sorted_data[:split_index]
        test_data = sorted_data[split_index:]
    
    return train_data, test_data

"""
Data analysis utilities for statistical analysis and exploratory data analysis.
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class DataAnalyzer:
    """Class for performing comprehensive data analysis."""
    
    def __init__(self, data):
        """
        Initialize the DataAnalyzer.
        
        Args:
            data: pandas DataFrame or file path to CSV
        """
        if isinstance(data, str):
            self.data = pd.read_csv(data)
        else:
            self.data = data.copy()
    
    def basic_stats(self):
        """Calculate basic statistical measures."""
        print("\n📊 Basic Statistics")
        print("-" * 30)
        
        # Dataset info
        print(f"Dataset shape: {self.data.shape}")
        print(f"Memory usage: {self.data.memory_usage(deep=True).sum() / 1024:.2f} KB")
        
        # Data types
        print("\nData types:")
        print(self.data.dtypes.value_counts())
        
        # Missing values
        missing = self.data.isnull().sum()
        if missing.sum() > 0:
            print("\nMissing values:")
            print(missing[missing > 0])
        else:
            print("\n✅ No missing values found")
        
        # Descriptive statistics for numeric columns
        numeric_data = self.data.select_dtypes(include=[np.number])
        if not numeric_data.empty:
            print("\nDescriptive Statistics (Numeric):")
            print(numeric_data.describe())
        
        # Categorical column summary
        categorical_data = self.data.select_dtypes(include=['object'])
        if not categorical_data.empty:
            print("\nCategorical Variables Summary:")
            for col in categorical_data.columns:
                unique_count = self.data[col].nunique()
                print(f"{col}: {unique_count} unique values")
                if unique_count <= 10:
                    print(f"  Values: {list(self.data[col].unique())}")
        
        return {
            'shape': self.data.shape,
            'missing_values': missing.to_dict(),
            'numeric_summary': numeric_data.describe().to_dict() if not numeric_data.empty else {},
            'categorical_summary': {col: self.data[col].value_counts().to_dict() 
                                  for col in categorical_data.columns}
        }
    
    def correlation_analysis(self):
        """Analyze correlations between numeric variables."""
        numeric_data = self.data.select_dtypes(include=[np.number])
        
        if numeric_data.shape[1] < 2:
            print("⚠️ Need at least 2 numeric columns for correlation analysis")
            return None
        
        print("\n🔗 Correlation Analysis")
        print("-" * 30)
        
        # Calculate correlation matrix
        corr_matrix = numeric_data.corr()
        
        # Find strong correlations (>0.7 or <-0.7)
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_correlations.append({
                        'var1': corr_matrix.columns[i],
                        'var2': corr_matrix.columns[j],
                        'correlation': corr_value
                    })
        
        if strong_correlations:
            print("Strong correlations found:")
            for corr in strong_correlations:
                print(f"  {corr['var1']} ↔ {corr['var2']}: {corr['correlation']:.3f}")
        else:
            print("No strong correlations (>0.7) found")
        
        return corr_matrix
    
    def detect_outliers(self, column, method='iqr'):
        """
        Detect outliers in a numeric column.
        
        Args:
            column: Column name
            method: 'iqr' or 'zscore'
        """
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found")
        
        if method == 'iqr':
            Q1 = self.data[column].quantile(0.25)
            Q3 = self.data[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = self.data[(self.data[column] < lower_bound) | 
                               (self.data[column] > upper_bound)]
        
        elif method == 'zscore':
            z_scores = np.abs(stats.zscore(self.data[column].dropna()))
            outliers = self.data[z_scores > 3]
        
        print(f"\n🎯 Outlier Detection ({method.upper()}) for '{column}'")
        print("-" * 40)
        print(f"Total outliers found: {len(outliers)}")
        print(f"Percentage of data: {len(outliers)/len(self.data)*100:.2f}%")
        
        return outliers
    
    def data_quality_report(self):
        """Generate a comprehensive data quality report."""
        print("\n📋 Data Quality Report")
        print("=" * 40)
        
        # Completeness
        completeness = (1 - self.data.isnull().sum() / len(self.data)) * 100
        print("\n1. Data Completeness:")
        for col in completeness.index:
            status = "✅" if completeness[col] == 100 else "⚠️" if completeness[col] > 90 else "❌"
            print(f"   {status} {col}: {completeness[col]:.1f}%")
        
        # Duplicates
        duplicates = self.data.duplicated().sum()
        print(f"\n2. Duplicate Rows: {duplicates}")
        
        # Data types consistency
        print("\n3. Data Types:")
        for dtype in self.data.dtypes.unique():
            cols = list(self.data.select_dtypes(include=[dtype]).columns)
            print(f"   {dtype}: {len(cols)} columns")
        
        return {
            'completeness': completeness.to_dict(),
            'duplicates': duplicates,
            'total_rows': len(self.data)
        }

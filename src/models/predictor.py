"""
Machine learning models for prediction and classification tasks.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class Predictor:
    """Class for machine learning prediction tasks."""
    
    def __init__(self):
        """Initialize the Predictor."""
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.categorical_encoders = {}
        self.is_classification = False
        self.feature_columns = None
        self.target_column = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_pred = None
    
    def train_model(self, data, feature_columns, target_column, model_type='auto', test_size=0.2):
        """
        Train a machine learning model.
        
        Args:
            data: pandas DataFrame
            feature_columns: list of feature column names
            target_column: target column name
            model_type: 'auto', 'linear', 'random_forest', 'logistic'
            test_size: proportion of data for testing
        """
        self.feature_columns = feature_columns
        self.target_column = target_column
        
        # Prepare features and target
        X = data[feature_columns].copy()
        y = data[target_column].copy()
        
        # Handle missing values more robustly
        # For numeric columns, use mean
        numeric_columns = X.select_dtypes(include=[np.number]).columns
        X[numeric_columns] = X[numeric_columns].fillna(X[numeric_columns].mean())
        
        # For categorical columns, use mode
        categorical_columns = X.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if X[col].isnull().sum() > 0:
                mode_value = X[col].mode()
                if len(mode_value) > 0:
                    X[col] = X[col].fillna(mode_value[0])
                else:
                    X[col] = X[col].fillna('Unknown')
        
        # Handle target variable missing values
        if y.isnull().sum() > 0:
            if y.dtype in ['float64', 'int64']:
                y = y.fillna(y.mean())
            else:
                mode_value = y.mode()
                if len(mode_value) > 0:
                    y = y.fillna(mode_value[0])
                else:
                    y = y.fillna('Unknown')
        
        # Determine if it's a classification problem
        if y.dtype == 'object' or y.nunique() <= 10:
            self.is_classification = True
            if y.dtype == 'object':
                y = self.label_encoder.fit_transform(y.astype(str))
        
        # Encode categorical features
        self.categorical_encoders = {}
        for col in categorical_columns:
            if col in X.columns:
                encoder = LabelEncoder()
                X[col] = encoder.fit_transform(X[col].astype(str))
                self.categorical_encoders[col] = encoder
        
        # Split the data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Scale features
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        # Choose model
        if model_type == 'auto':
            if self.is_classification:
                self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            else:
                self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        elif model_type == 'linear':
            self.model = LinearRegression()
        elif model_type == 'random_forest':
            if self.is_classification:
                self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            else:
                self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        elif model_type == 'logistic':
            self.model = LogisticRegression(random_state=42)
        
        # Train the model
        print(f"🤖 Training {'classification' if self.is_classification else 'regression'} model...")
        
        if model_type in ['linear', 'logistic']:
            self.model.fit(self.X_train_scaled, self.y_train)
            self.y_pred = self.model.predict(self.X_test_scaled)
        else:
            self.model.fit(self.X_train, self.y_train)
            self.y_pred = self.model.predict(self.X_test)
        
        # Evaluate model
        performance = self._evaluate_model()
        
        return performance
    
    def _evaluate_model(self):
        """Evaluate the trained model."""
        if self.is_classification:
            accuracy = accuracy_score(self.y_test, self.y_pred)
            print(f"✅ Model Accuracy: {accuracy:.4f}")
            
            # Classification report
            if hasattr(self.label_encoder, 'classes_'):
                target_names = self.label_encoder.classes_
            else:
                target_names = None
            
            report = classification_report(self.y_test, self.y_pred, 
                                         target_names=target_names, output_dict=True)
            
            return {
                'accuracy': accuracy,
                'classification_report': report,
                'model_type': 'classification'
            }
        else:
            mse = mean_squared_error(self.y_test, self.y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(self.y_test, self.y_pred)
            
            print(f"✅ Model Performance:")
            print(f"   R² Score: {r2:.4f}")
            print(f"   RMSE: {rmse:.4f}")
            print(f"   MSE: {mse:.4f}")
            
            return {
                'r2_score': r2,
                'rmse': rmse,
                'mse': mse,
                'model_type': 'regression'
            }
    
    def predict(self, new_data):
        """
        Make predictions on new data.
        
        Args:
            new_data: pandas DataFrame with same features as training data
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train_model() first.")
        
        # Prepare features
        X_new = new_data[self.feature_columns].copy()
        
        # Handle missing values
        numeric_columns = X_new.select_dtypes(include=[np.number]).columns
        X_new[numeric_columns] = X_new[numeric_columns].fillna(X_new[numeric_columns].mean())
        
        categorical_columns = X_new.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if X_new[col].isnull().sum() > 0:
                X_new[col] = X_new[col].fillna('Unknown')
        
        # Apply categorical encoding if available
        if hasattr(self, 'categorical_encoders'):
            for col, encoder in self.categorical_encoders.items():
                if col in X_new.columns:
                    # Handle unseen categories
                    try:
                        X_new[col] = encoder.transform(X_new[col].astype(str))
                    except ValueError:
                        # If unseen categories, map them to the most frequent class
                        X_new[col] = X_new[col].astype(str)
                        unseen_mask = ~X_new[col].isin(encoder.classes_)
                        if unseen_mask.any():
                            most_frequent = encoder.classes_[0]  # Use first class as default
                            X_new.loc[unseen_mask, col] = most_frequent
                        X_new[col] = encoder.transform(X_new[col])
        
        # Make predictions
        if isinstance(self.model, (LinearRegression, LogisticRegression)):
            X_new_scaled = self.scaler.transform(X_new)
            predictions = self.model.predict(X_new_scaled)
        else:
            predictions = self.model.predict(X_new)
        
        # Convert back to original labels if classification
        if self.is_classification and hasattr(self.label_encoder, 'classes_'):
            predictions = self.label_encoder.inverse_transform(predictions.astype(int))
        
        return predictions
    
    def get_feature_importance(self):
        """Get feature importance for tree-based models."""
        if hasattr(self.model, 'feature_importances_'):
            importance_df = pd.DataFrame({
                'feature': self.feature_columns,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print("\n📊 Feature Importance:")
            print("-" * 30)
            for _, row in importance_df.iterrows():
                print(f"  {row['feature']}: {row['importance']:.4f}")
            
            return importance_df
        else:
            print("⚠️ Feature importance not available for this model type")
            return None
    
    def cross_validate(self, cv_folds=5):
        """Perform cross-validation."""
        if self.model is None:
            raise ValueError("Model not trained yet. Call train_model() first.")
        
        print(f"\n🔄 Performing {cv_folds}-fold cross-validation...")
        
        # Prepare data
        X = pd.concat([pd.DataFrame(self.X_train), pd.DataFrame(self.X_test)])
        y = pd.concat([pd.Series(self.y_train), pd.Series(self.y_test)])
        
        # Perform cross-validation
        if self.is_classification:
            scores = cross_val_score(self.model, X, y, cv=cv_folds, scoring='accuracy')
            print(f"✅ Cross-validation Accuracy: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")
        else:
            scores = cross_val_score(self.model, X, y, cv=cv_folds, scoring='r2')
            print(f"✅ Cross-validation R² Score: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")
        
        return scores

"""
Visualization utilities for creating charts and graphs.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style for matplotlib
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class Plotter:
    """Class for creating various types of plots and visualizations."""
    
    def __init__(self, figsize=(10, 6)):
        """
        Initialize the Plotter.
        
        Args:
            figsize: Default figure size for matplotlib plots
        """
        self.figsize = figsize
        
    def plot_distribution(self, data, column, plot_type='hist', save_path=None):
        """
        Plot distribution of a numeric column.
        
        Args:
            data: pandas DataFrame
            column: column name
            plot_type: 'hist', 'box', 'violin', or 'kde'
            save_path: path to save the plot
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Distribution Analysis: {column}', fontsize=16, fontweight='bold')
        
        # Histogram
        axes[0, 0].hist(data[column].dropna(), bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('Histogram')
        axes[0, 0].set_xlabel(column)
        axes[0, 0].set_ylabel('Frequency')
        
        # Box plot
        data[column].dropna().plot(kind='box', ax=axes[0, 1])
        axes[0, 1].set_title('Box Plot')
        axes[0, 1].set_ylabel(column)
        
        # KDE plot
        data[column].dropna().plot(kind='kde', ax=axes[1, 0], color='red')
        axes[1, 0].set_title('Kernel Density Estimation')
        axes[1, 0].set_xlabel(column)
        axes[1, 0].set_ylabel('Density')
        
        # Q-Q plot
        from scipy import stats
        stats.probplot(data[column].dropna(), dist="norm", plot=axes[1, 1])
        axes[1, 1].set_title('Q-Q Plot (Normal Distribution)')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Distribution plot saved to {save_path}")
        
        plt.show()
    
    def plot_correlation_heatmap(self, data, save_path=None):
        """
        Create a correlation heatmap for numeric columns.
        
        Args:
            data: pandas DataFrame
            save_path: path to save the plot
        """
        # Select only numeric columns
        numeric_data = data.select_dtypes(include=[np.number])
        
        if numeric_data.empty:
            print("⚠️ No numeric columns found for correlation heatmap")
            return
        
        # Calculate correlation matrix
        corr_matrix = numeric_data.corr()
        
        # Create heatmap
        plt.figure(figsize=(12, 10))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        
        sns.heatmap(corr_matrix, 
                   mask=mask,
                   annot=True, 
                   cmap='coolwarm', 
                   center=0,
                   square=True,
                   fmt='.2f',
                   cbar_kws={"shrink": .8})
        
        plt.title('Correlation Heatmap', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"🔥 Correlation heatmap saved to {save_path}")
        
        plt.show()
    
    def plot_scatter(self, data, x_col, y_col, color_col=None, save_path=None):
        """
        Create scatter plot between two variables.
        
        Args:
            data: pandas DataFrame
            x_col: x-axis column name
            y_col: y-axis column name
            color_col: column for color coding (optional)
            save_path: path to save the plot
        """
        plt.figure(figsize=self.figsize)
        
        if color_col and color_col in data.columns:
            scatter = plt.scatter(data[x_col], data[y_col], c=data[color_col], 
                                alpha=0.6, cmap='viridis')
            plt.colorbar(scatter, label=color_col)
        else:
            plt.scatter(data[x_col], data[y_col], alpha=0.6, color='blue')
        
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(f'Scatter Plot: {x_col} vs {y_col}')
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📈 Scatter plot saved to {save_path}")
        
        plt.show()
    
    def plot_predictions(self, actual, predicted, save_path=None):
        """
        Plot actual vs predicted values.
        
        Args:
            actual: actual values
            predicted: predicted values
            save_path: path to save the plot
        """
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Actual vs Predicted scatter plot
        axes[0].scatter(actual, predicted, alpha=0.6, color='blue')
        
        # Perfect prediction line
        min_val = min(min(actual), min(predicted))
        max_val = max(max(actual), max(predicted))
        axes[0].plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
        
        axes[0].set_xlabel('Actual Values')
        axes[0].set_ylabel('Predicted Values')
        axes[0].set_title('Actual vs Predicted')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Residuals plot
        residuals = actual - predicted
        axes[1].scatter(predicted, residuals, alpha=0.6, color='red')
        axes[1].axhline(y=0, color='black', linestyle='-', alpha=0.8)
        axes[1].set_xlabel('Predicted Values')
        axes[1].set_ylabel('Residuals')
        axes[1].set_title('Residuals Plot')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"🎯 Prediction plot saved to {save_path}")
        
        plt.show()
    
    def plot_feature_importance(self, importance_df, save_path=None):
        """
        Plot feature importance.
        
        Args:
            importance_df: DataFrame with 'feature' and 'importance' columns
            save_path: path to save the plot
        """
        plt.figure(figsize=(10, max(6, len(importance_df) * 0.4)))
        
        colors = plt.cm.viridis(np.linspace(0, 1, len(importance_df)))
        bars = plt.barh(importance_df['feature'], importance_df['importance'], color=colors)
        
        plt.xlabel('Importance')
        plt.title('Feature Importance', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        
        # Add value labels on bars
        for bar, importance in zip(bars, importance_df['importance']):
            plt.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2, 
                    f'{importance:.3f}', ha='left', va='center')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Feature importance plot saved to {save_path}")
        
        plt.show()
    
    def plot_time_series(self, data, date_col, value_col, save_path=None):
        """
        Plot time series data.
        
        Args:
            data: pandas DataFrame
            date_col: date column name
            value_col: value column name
            save_path: path to save the plot
        """
        # Convert date column to datetime
        data[date_col] = pd.to_datetime(data[date_col])
        
        plt.figure(figsize=(14, 6))
        plt.plot(data[date_col], data[value_col], linewidth=2, color='blue')
        
        plt.xlabel('Date')
        plt.ylabel(value_col)
        plt.title(f'Time Series: {value_col}')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📅 Time series plot saved to {save_path}")
        
        plt.show()
    
    def create_interactive_plot(self, data, x_col, y_col, color_col=None, plot_type='scatter'):
        """
        Create interactive plots using Plotly.
        
        Args:
            data: pandas DataFrame
            x_col: x-axis column name
            y_col: y-axis column name
            color_col: column for color coding (optional)
            plot_type: 'scatter', 'line', 'bar'
        """
        if plot_type == 'scatter':
            fig = px.scatter(data, x=x_col, y=y_col, color=color_col,
                           title=f'Interactive Scatter: {x_col} vs {y_col}',
                           hover_data=data.columns)
        elif plot_type == 'line':
            fig = px.line(data, x=x_col, y=y_col, color=color_col,
                         title=f'Interactive Line: {x_col} vs {y_col}')
        elif plot_type == 'bar':
            fig = px.bar(data, x=x_col, y=y_col, color=color_col,
                        title=f'Interactive Bar: {x_col} vs {y_col}')
        
        fig.update_layout(
            width=800,
            height=600,
            hovermode='closest'
        )
        
        fig.show()
        return fig
    
    def plot_multiple_distributions(self, data, columns, save_path=None):
        """
        Plot distributions of multiple columns in subplots.
        
        Args:
            data: pandas DataFrame
            columns: list of column names
            save_path: path to save the plot
        """
        n_cols = min(3, len(columns))
        n_rows = (len(columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(5*n_cols, 4*n_rows))
        
        if n_rows == 1:
            axes = [axes] if n_cols == 1 else axes
        elif n_cols == 1:
            axes = [[ax] for ax in axes]
        
        for i, col in enumerate(columns):
            row = i // n_cols
            col_idx = i % n_cols
            
            if n_rows == 1:
                ax = axes[col_idx] if n_cols > 1 else axes[0]
            else:
                ax = axes[row][col_idx] if n_cols > 1 else axes[row][0]
            
            data[col].hist(bins=30, alpha=0.7, ax=ax)
            ax.set_title(f'Distribution of {col}')
            ax.set_xlabel(col)
            ax.set_ylabel('Frequency')
        
        # Hide empty subplots
        for i in range(len(columns), n_rows * n_cols):
            row = i // n_cols
            col_idx = i % n_cols
            if n_rows == 1:
                ax = axes[col_idx] if n_cols > 1 else axes[0]
            else:
                ax = axes[row][col_idx] if n_cols > 1 else axes[row][0]
            ax.set_visible(False)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Multiple distributions plot saved to {save_path}")
        
        plt.show()

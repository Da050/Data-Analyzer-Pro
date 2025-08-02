"""
Flask web application for interactive data analysis and prediction.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
import pandas as pd
import numpy as np
import os
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from werkzeug.utils import secure_filename
import json
from datetime import datetime

# Import our custom modules
import sys
sys.path.append('src')
from analysis.data_analyzer import DataAnalyzer
from models.predictor import Predictor
from visualization.plotter import Plotter
from utils.data_generator import generate_sample_data
from config import config

app = Flask(__name__)

# Configure app based on environment
config_name = os.environ.get('FLASK_ENV', 'default')
app.config.from_object(config[config_name])

# Ensure directories exist
os.makedirs('uploads', exist_ok=True)
os.makedirs('outputs', exist_ok=True)
os.makedirs('static/plots', exist_ok=True)

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_plot_base64(fig):
    """Convert matplotlib figure to base64 string."""
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight', dpi=300)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    return plot_url

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Handle file upload and initial analysis."""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename or 'uploaded_file')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Load the data
                if filename.endswith('.csv'):
                    data = pd.read_csv(filepath)
                else:
                    data = pd.read_excel(filepath)
                
                # Store basic info in session (simplified for demo)
                session_data = {
                    'filename': filename,
                    'shape': data.shape,
                    'columns': data.columns.tolist(),
                    'dtypes': data.dtypes.astype(str).to_dict(),
                    'head': data.head().to_dict(),
                    'missing': data.isnull().sum().to_dict()
                }
                
                return render_template('analysis.html', 
                                     data_info=session_data, 
                                     filename=filename)
                
            except Exception as e:
                flash(f'Error processing file: {str(e)}')
                return redirect(url_for('upload_file'))
        else:
            flash('Invalid file type. Please upload CSV or Excel files.')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.route('/generate_sample')
def generate_sample():
    """Generate sample data for demonstration."""
    try:
        # Generate sample data
        sample_file = os.path.join(app.config['UPLOAD_FOLDER'], 'sample_data.csv')
        data = generate_sample_data(sample_file, n_samples=500)
        
        session_data = {
            'filename': 'sample_data.csv',
            'shape': data.shape,
            'columns': data.columns.tolist(),
            'dtypes': data.dtypes.astype(str).to_dict(),
            'head': data.head().to_dict(),
            'missing': data.isnull().sum().to_dict()
        }
        
        flash('Sample data generated successfully!')
        return render_template('analysis.html', 
                             data_info=session_data, 
                             filename='sample_data.csv')
    
    except Exception as e:
        flash(f'Error generating sample data: {str(e)}')
        return redirect(url_for('index'))

@app.route('/analyze/<filename>')
def analyze_data(filename):
    """Perform comprehensive data analysis."""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if filename.endswith('.csv'):
            data = pd.read_csv(filepath)
        else:
            data = pd.read_excel(filepath)
        
        # Initialize analyzer
        analyzer = DataAnalyzer(data)
        
        # Basic statistics
        stats = analyzer.basic_stats()
        
        # Correlation analysis
        corr_matrix = analyzer.correlation_analysis()
        
        # Data quality report
        quality_report = analyzer.data_quality_report()
        
        # Generate visualizations
        plots = {}
        
        # Distribution plots for numeric columns
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) > 0:
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Data Distributions', fontsize=16)
            
            for i, col in enumerate(numeric_columns[:4]):
                row, col_idx = divmod(i, 2)
                data[col].hist(bins=30, ax=axes[row, col_idx], alpha=0.7)
                axes[row, col_idx].set_title(f'Distribution of {col}')
                axes[row, col_idx].set_xlabel(col)
                axes[row, col_idx].set_ylabel('Frequency')
            
            # Hide empty subplots
            for i in range(len(numeric_columns), 4):
                row, col_idx = divmod(i, 2)
                axes[row, col_idx].set_visible(False)
            
            plt.tight_layout()
            plots['distributions'] = create_plot_base64(fig)
        
        # Correlation heatmap
        if len(numeric_columns) > 1:
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(data[numeric_columns].corr(), 
                       annot=True, cmap='coolwarm', center=0,
                       square=True, fmt='.2f', ax=ax)
            ax.set_title('Correlation Heatmap')
            plt.tight_layout()
            plots['correlation'] = create_plot_base64(fig)
        
        return render_template('results.html',
                             filename=filename,
                             stats=stats,
                             quality_report=quality_report,
                             plots=plots,
                             columns=data.columns.tolist(),
                             numeric_columns=numeric_columns.tolist())
    
    except Exception as e:
        flash(f'Error analyzing data: {str(e)}')
        return redirect(url_for('index'))

@app.route('/predict/<filename>')
def predict_page(filename):
    """Show prediction interface."""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if filename.endswith('.csv'):
            data = pd.read_csv(filepath)
        else:
            data = pd.read_excel(filepath)
        
        numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_columns = data.select_dtypes(include=['object']).columns.tolist()
        
        return render_template('predict.html',
                             filename=filename,
                             numeric_columns=numeric_columns,
                             categorical_columns=categorical_columns,
                             all_columns=data.columns.tolist())
    
    except Exception as e:
        flash(f'Error loading prediction page: {str(e)}')
        return redirect(url_for('index'))

@app.route('/run_prediction', methods=['POST'])
def run_prediction():
    """Execute machine learning prediction."""
    try:
        filename = request.form['filename']
        feature_columns = request.form.getlist('features')
        target_column = request.form['target']
        model_type = request.form['model_type']
        
        # Validation
        if not feature_columns:
            flash('Please select at least one feature column.')
            return redirect(url_for('predict_page', filename=filename))
        
        if not target_column:
            flash('Please select a target column.')
            return redirect(url_for('predict_page', filename=filename))
        
        if target_column in feature_columns:
            flash('Target column cannot be used as a feature. Please remove it from features.')
            return redirect(url_for('predict_page', filename=filename))
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if filename.endswith('.csv'):
            data = pd.read_csv(filepath)
        else:
            data = pd.read_excel(filepath)
        
        # Check if selected columns exist
        missing_columns = []
        for col in feature_columns + [target_column]:
            if col not in data.columns:
                missing_columns.append(col)
        
        if missing_columns:
            flash(f'Missing columns in dataset: {", ".join(missing_columns)}')
            return redirect(url_for('predict_page', filename=filename))
        
        # Check if we have enough data
        if len(data) < 10:
            flash('Dataset too small. Need at least 10 rows for training.')
            return redirect(url_for('predict_page', filename=filename))
        
        # Initialize predictor
        predictor = Predictor()
        
        # Train model
        performance = predictor.train_model(
            data, feature_columns, target_column, model_type=model_type
        )
        
        # Generate prediction plots
        plots = {}
        
        # Only create regression plots for regression models
        if performance['model_type'] == 'regression':
            # Actual vs Predicted plot
            fig, axes = plt.subplots(1, 2, figsize=(15, 6))
            
            # Actual vs Predicted scatter
            axes[0].scatter(predictor.y_test, predictor.y_pred, alpha=0.6)
            min_val = min(min(predictor.y_test), min(predictor.y_pred))
            max_val = max(max(predictor.y_test), max(predictor.y_pred))
            axes[0].plot([min_val, max_val], [min_val, max_val], 'r--', lw=2)
            axes[0].set_xlabel('Actual Values')
            axes[0].set_ylabel('Predicted Values')
            axes[0].set_title('Actual vs Predicted')
            axes[0].grid(True, alpha=0.3)
            
            # Residuals plot
            residuals = predictor.y_test - predictor.y_pred
            axes[1].scatter(predictor.y_pred, residuals, alpha=0.6, color='red')
            axes[1].axhline(y=0, color='black', linestyle='-')
            axes[1].set_xlabel('Predicted Values')
            axes[1].set_ylabel('Residuals')
            axes[1].set_title('Residuals Plot')
            axes[1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            plots['predictions'] = create_plot_base64(fig)
        else:
            # For classification, create confusion matrix-style plot
            from sklearn.metrics import confusion_matrix
            import seaborn as sns
            
            # Get unique labels
            unique_labels = np.unique(np.concatenate([predictor.y_test, predictor.y_pred]))
            cm = confusion_matrix(predictor.y_test, predictor.y_pred, labels=unique_labels)
            
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
            ax.set_xlabel('Predicted')
            ax.set_ylabel('Actual')
            ax.set_title('Confusion Matrix')
            
            plt.tight_layout()
            plots['predictions'] = create_plot_base64(fig)
        
        # Feature importance (if available)
        importance_df = predictor.get_feature_importance()
        if importance_df is not None and len(importance_df) > 0:
            try:
                fig, ax = plt.subplots(figsize=(10, max(6, len(importance_df) * 0.4)))
                bars = ax.barh(importance_df['feature'], importance_df['importance'])
                ax.set_xlabel('Importance')
                ax.set_title('Feature Importance')
                ax.invert_yaxis()
                
                # Add value labels
                for bar, importance in zip(bars, importance_df['importance']):
                    ax.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2, 
                           f'{importance:.3f}', ha='left', va='center')
                
                plt.tight_layout()
                plots['feature_importance'] = create_plot_base64(fig)
            except Exception as e:
                print(f"Warning: Could not create feature importance plot: {e}")
                # Continue without feature importance plot
        
        return render_template('prediction_results.html',
                             filename=filename,
                             performance=performance,
                             plots=plots,
                             feature_columns=feature_columns,
                             target_column=target_column,
                             model_type=model_type)
    
    except ValueError as ve:
        flash(f'Data validation error: {str(ve)}')
        return redirect(url_for('predict_page', filename=filename))
    
    except Exception as e:
        flash(f'Error running prediction: {str(e)}')
        return redirect(url_for('predict_page', filename=filename))

@app.route('/api/data_preview/<filename>')
def api_data_preview(filename):
    """API endpoint to get data preview."""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if filename.endswith('.csv'):
            data = pd.read_csv(filepath)
        else:
            data = pd.read_excel(filepath)
        
        preview = {
            'shape': data.shape,
            'columns': data.columns.tolist(),
            'head': data.head(10).to_dict('records'),
            'dtypes': data.dtypes.astype(str).to_dict(),
            'missing': data.isnull().sum().to_dict()
        }
        
        return jsonify(preview)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/download_sample')
def download_sample():
    """Download sample dataset."""
    try:
        sample_file = 'sample_download.csv'
        sample_path = os.path.join('data', sample_file)
        
        # Generate fresh sample data
        generate_sample_data(sample_path, n_samples=1000)
        
        return send_file(sample_path, as_attachment=True, download_name='sample_data.csv')
    
    except Exception as e:
        flash(f'Error downloading sample: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

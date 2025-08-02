"""
Main entry point for the Data Analysis and Prediction Project.
"""

import os
import sys
import pandas as pd
from analysis.data_analyzer import DataAnalyzer
from models.predictor import Predictor
from visualization.plotter import Plotter
from utils.data_generator import generate_sample_data

def main():
    """Main function to demonstrate the project capabilities."""
    
    print("🔍 Data Analysis and Prediction Project")
    print("=" * 50)
    
    # Ensure output directory exists
    os.makedirs('outputs', exist_ok=True)
    
    # Generate sample data if it doesn't exist
    data_file = 'data/sample_data.csv'
    if not os.path.exists(data_file):
        print("📊 Generating sample data...")
        generate_sample_data()
    
    # Load data
    print("📁 Loading data...")
    data = pd.read_csv(data_file)
    print(f"✅ Loaded {len(data)} rows of data")
    
    # Perform data analysis
    print("\n📈 Performing data analysis...")
    analyzer = DataAnalyzer(data)
    stats = analyzer.basic_stats()
    print("✅ Basic statistics calculated")
    
    # Create visualizations
    print("\n📊 Creating visualizations...")
    plotter = Plotter()
    
    # Distribution plots
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_columns) > 0:
        plotter.plot_distribution(data, numeric_columns[0], save_path='outputs/distribution.png')
        print("✅ Distribution plot saved")
    
    # Correlation heatmap
    if len(numeric_columns) > 1:
        plotter.plot_correlation_heatmap(data, save_path='outputs/correlation_heatmap.png')
        print("✅ Correlation heatmap saved")
    
    # Machine learning prediction
    if len(numeric_columns) >= 2:
        print("\n🤖 Training prediction model...")
        predictor = Predictor()
        target_column = numeric_columns[-1]  # Use last numeric column as target
        feature_columns = numeric_columns[:-1].tolist()
        
        # Train model
        model_performance = predictor.train_model(data, feature_columns, target_column)
        print(f"✅ Model trained - R² Score: {model_performance['r2_score']:.4f}")
        
        # Create prediction plots
        plotter.plot_predictions(
            predictor.y_test, 
            predictor.y_pred, 
            save_path='outputs/predictions.png'
        )
        print("✅ Prediction plot saved")
    
    print("\n🎉 Analysis complete! Check the 'outputs' folder for visualizations.")

if __name__ == "__main__":
    main()

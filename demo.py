"""
Complete demonstration of the Data Analysis and Prediction Platform
"""

import os
import sys
sys.path.append('src')

from analysis.data_analyzer import DataAnalyzer
from models.predictor import Predictor
from visualization.plotter import Plotter
from utils.data_generator import generate_sample_data

def main():
    """Run a complete demonstration of all features."""
    
    print("🚀 Data Analysis and Prediction Platform Demo")
    print("=" * 60)
    
    # 1. Generate sample data
    print("\n1️⃣ Generating sample dataset...")
    data_file = 'data/demo_data.csv'
    os.makedirs('data', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    
    data = generate_sample_data(data_file, n_samples=500)
    
    # 2. Data Analysis
    print("\n2️⃣ Performing comprehensive data analysis...")
    analyzer = DataAnalyzer(data)
    
    # Basic statistics
    stats = analyzer.basic_stats()
    
    # Correlation analysis
    corr_matrix = analyzer.correlation_analysis()
    
    # Data quality report
    quality_report = analyzer.data_quality_report()
    
    # 3. Visualizations
    print("\n3️⃣ Creating visualizations...")
    plotter = Plotter()
    
    # Distribution of income
    plotter.plot_distribution(data, 'income', save_path='outputs/demo_distribution.png')
    
    # Correlation heatmap
    plotter.plot_correlation_heatmap(data, save_path='outputs/demo_correlation.png')
    
    # Scatter plot
    plotter.plot_scatter(data, 'age', 'income', color_col='department', 
                        save_path='outputs/demo_scatter.png')
    
    # 4. Machine Learning - Regression
    print("\n4️⃣ Building regression model...")
    predictor_reg = Predictor()
    
    # Predict income based on age, education, and experience
    feature_columns = ['age', 'education_years', 'experience_years']
    target_column = 'income'
    
    performance_reg = predictor_reg.train_model(
        data, feature_columns, target_column, model_type='random_forest'
    )
    
    # Plot predictions
    plotter.plot_predictions(
        predictor_reg.y_test, 
        predictor_reg.y_pred, 
        save_path='outputs/demo_predictions.png'
    )
    
    # Feature importance
    importance_df = predictor_reg.get_feature_importance()
    if importance_df is not None:
        plotter.plot_feature_importance(importance_df, 
                                       save_path='outputs/demo_feature_importance.png')
    
    # 5. Machine Learning - Classification
    print("\n5️⃣ Building classification model...")
    predictor_cls = Predictor()
    
    # Predict performance rating
    feature_columns_cls = ['age', 'education_years', 'experience_years', 'satisfaction_score']
    target_column_cls = 'performance_rating'
    
    # Clean data for classification
    clean_data = data.dropna()
    
    performance_cls = predictor_cls.train_model(
        clean_data, feature_columns_cls, target_column_cls, model_type='random_forest'
    )
    
    # 6. Summary
    print("\n6️⃣ Demo Summary")
    print("=" * 40)
    print(f"📊 Dataset: {data.shape[0]} rows, {data.shape[1]} columns")
    print(f"📈 Regression R² Score: {performance_reg['r2_score']:.4f}")
    print(f"🎯 Classification Accuracy: {performance_cls['accuracy']:.4f}")
    print(f"📁 Visualizations saved to outputs/ folder")
    
    print("\n🎉 Demo completed successfully!")
    print("\n🌐 To try the web interface, run: python app.py")
    print("   Then open http://localhost:5000 in your browser")
    
    # 7. Web app info
    print("\n" + "=" * 60)
    print("🌟 WEB APPLICATION FEATURES:")
    print("=" * 60)
    print("✅ Upload CSV/Excel files")
    print("✅ Interactive data analysis")
    print("✅ Automatic visualizations")
    print("✅ Point-and-click ML modeling")
    print("✅ Download results and reports")
    print("✅ No coding required!")
    print("=" * 60)

if __name__ == "__main__":
    main()

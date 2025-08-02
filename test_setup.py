"""
Test script to verify the project setup and functionality.
"""

import sys
import os
sys.path.append('src')

def test_imports():
    """Test if all modules can be imported."""
    try:
        from analysis.data_analyzer import DataAnalyzer
        from models.predictor import Predictor
        from visualization.plotter import Plotter
        from utils.data_generator import generate_sample_data
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_generation():
    """Test data generation functionality."""
    try:
        os.makedirs('data', exist_ok=True)
        from utils.data_generator import generate_sample_data
        data = generate_sample_data('data/test_data.csv', n_samples=100)
        print("✅ Data generation successful")
        return True
    except Exception as e:
        print(f"❌ Data generation error: {e}")
        return False

def test_analysis():
    """Test data analysis functionality."""
    try:
        import pandas as pd
        from analysis.data_analyzer import DataAnalyzer
        
        # Load test data
        data = pd.read_csv('data/test_data.csv')
        analyzer = DataAnalyzer(data)
        stats = analyzer.basic_stats()
        print("✅ Data analysis successful")
        return True
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Running Project Tests")
    print("=" * 30)
    
    tests = [
        ("Import Test", test_imports),
        ("Data Generation Test", test_data_generation),
        ("Analysis Test", test_analysis)
    ]
    
    passed = 0
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        if test_func():
            passed += 1
    
    print(f"\n📊 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Project is ready to use.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()

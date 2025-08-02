# Data Analysis and Prediction Project

A comprehensive Python project for data analysis, prediction, and visualization.

## Features

- **🌐 Web Interface**: User-friendly web application for non-programmers
- **📊 Data Analysis**: Statistical analysis and exploratory data analysis
- **🤖 Machine Learning**: Predictive modeling with various algorithms
- **📈 Visualization**: Interactive charts and graphs using matplotlib, seaborn, and plotly
- **🔧 Data Processing**: Clean and preprocess datasets
- **📋 Model Evaluation**: Performance metrics and validation
- **📁 Multiple Formats**: Support for CSV and Excel files
- **🎯 Auto ML**: Automatic model selection based on data type

## Project Structure

```
├── data/                   # Data files (CSV, JSON, etc.)
├── src/                    # Source code
│   ├── analysis/          # Data analysis modules
│   ├── models/            # Machine learning models
│   ├── visualization/     # Plotting and visualization
│   └── utils/             # Utility functions
├── notebooks/             # Jupyter notebooks for exploration
├── outputs/               # Generated plots and results
├── tests/                 # Unit tests
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the main analysis**:
   ```bash
   python src/main.py
   ```

3. **Start Jupyter notebook** (optional):
   ```bash
   jupyter notebook
   ```

## Usage

### 🌐 Web Interface (Recommended)

Start the web application:
```bash
python app.py
```

Then open your browser to `http://localhost:5000` to access the interactive web interface where you can:

- **Upload your data** (CSV, Excel files)
- **Generate sample datasets** for testing
- **Perform automatic analysis** with beautiful visualizations
- **Build machine learning models** with just a few clicks
- **Download results and reports**

### 📊 Python API

#### Basic Data Analysis
```python
from src.analysis.data_analyzer import DataAnalyzer

# Load and analyze data
analyzer = DataAnalyzer('data/sample_data.csv')
analyzer.basic_stats()
analyzer.correlation_analysis()
```

#### Prediction Models
```python
from src.models.predictor import Predictor

# Create and train a model
predictor = Predictor()
predictor.load_data('data/sample_data.csv')
predictor.train_model()
predictions = predictor.predict(new_data)
```

#### Visualization
```python
from src.visualization.plotter import Plotter

# Generate visualizations
plotter = Plotter()
plotter.plot_distribution(data, 'column_name')
plotter.plot_correlation_heatmap(data)
plotter.plot_predictions(actual, predicted)
```

## 🚀 Deployment

This application is ready for live deployment! See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to various platforms.

### Quick Deployment Options:

- **Heroku**: `git push heroku main` (after setup)
- **Render**: Connect GitHub repo and deploy
- **Railway**: Connect GitHub repo and deploy
- **Docker**: `docker build -t dataapp . && docker run -p 5000:5000 dataapp`

### Production Testing

Test the app with production settings locally:

**Windows:**
```bash
run_production.bat
```

**Linux/Mac:**
```bash
chmod +x run_production.sh
./run_production.sh
```

## Sample Data

The project includes sample datasets in the `data/` folder for testing and demonstration purposes.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License

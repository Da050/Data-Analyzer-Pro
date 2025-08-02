"""
Deployment readiness checker for the Data Analysis Web App.
"""

import os
import sys
import importlib.util

def check_files():
    """Check if all required files exist."""
    required_files = [
        'app.py', 'wsgi.py', 'config.py', 'requirements.txt',
        'Procfile', 'Dockerfile', 'docker-compose.yml',
        'DEPLOYMENT.md', 'README.md'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required files present")
        return True

def check_dependencies():
    """Check if all required dependencies can be imported."""
    required_packages = [
        'flask', 'pandas', 'numpy', 'matplotlib', 
        'seaborn', 'sklearn', 'plotly', 'scipy'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'sklearn':
                importlib.import_module('sklearn')
            else:
                importlib.import_module(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nRun: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages installed")
        return True

def check_directories():
    """Check if all required directories exist."""
    required_dirs = [
        'src', 'src/analysis', 'src/models', 'src/visualization', 'src/utils',
        'templates', 'static', 'uploads', 'data', 'outputs'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print("❌ Missing required directories:")
        for dir_path in missing_dirs:
            print(f"   - {dir_path}")
        return False
    else:
        print("✅ All required directories present")
        return True

def check_environment():
    """Check environment configuration."""
    env_checks = []
    
    # Check Python version
    if sys.version_info >= (3, 8):
        print("✅ Python version compatible (>= 3.8)")
        env_checks.append(True)
    else:
        print(f"❌ Python version too old: {sys.version}")
        print("   Requires Python 3.8 or higher")
        env_checks.append(False)
    
    # Check if we can import the app
    try:
        sys.path.append('src')
        from app import app
        print("✅ Flask app can be imported")
        env_checks.append(True)
    except Exception as e:
        print(f"❌ Cannot import Flask app: {e}")
        env_checks.append(False)
    
    return all(env_checks)

def main():
    """Run all deployment readiness checks."""
    print("🚀 Deployment Readiness Check")
    print("=" * 40)
    
    checks = [
        check_files(),
        check_directories(),
        check_dependencies(),
        check_environment()
    ]
    
    print("\n" + "=" * 40)
    
    if all(checks):
        print("🎉 Your app is ready for deployment!")
        print("\nNext steps:")
        print("1. Choose a deployment platform (see DEPLOYMENT.md)")
        print("2. Set your SECRET_KEY environment variable")
        print("3. Deploy and test!")
    else:
        print("⚠️  Please fix the issues above before deploying")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

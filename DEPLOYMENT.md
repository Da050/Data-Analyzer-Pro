# Deployment Guide

This document provides step-by-step instructions for deploying the Data Analysis & Prediction Web App to various platforms.

## Prerequisites

- Python 3.12 or higher
- Git (for version control)
- Account on chosen deployment platform

## Local Testing with Production Settings

Before deploying, test the app with production settings:

**Windows:**
```bash
# Set environment variables
set FLASK_ENV=production
set SECRET_KEY=your-very-secure-secret-key

# Install dependencies
pip install -r requirements.txt

# Run with Waitress (Windows-compatible production server)
waitress-serve --host=0.0.0.0 --port=8000 wsgi:app
```

**Linux/Mac:**
```bash
# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=your-very-secure-secret-key

# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn (Unix production server)
gunicorn --bind 0.0.0.0:8000 wsgi:app
```

Visit `http://localhost:8000` to test the app.

## Deployment Options

### 1. Heroku Deployment

1. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```

2. **Create a new Heroku app**:
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**:
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=your-very-secure-secret-key
   ```

4. **Deploy**:
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push heroku main
   ```

5. **Open your app**:
   ```bash
   heroku open
   ```

### 2. Render Deployment

1. **Connect your GitHub repository** to Render
2. **Create a new Web Service** with these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app`
   - Environment Variables:
     - `FLASK_ENV=production`
     - `SECRET_KEY=your-very-secure-secret-key`

### 3. Railway Deployment

1. **Connect your GitHub repository** to Railway
2. **Set environment variables**:
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-very-secure-secret-key`
3. Railway will automatically detect and deploy your Flask app

### 4. DigitalOcean App Platform

1. **Create a new app** from your GitHub repository
2. **Configure the service**:
   - Source: Your GitHub repo
   - Type: Web Service
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn wsgi:app`
3. **Set environment variables**:
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-very-secure-secret-key`

### 5. Docker Deployment

For any platform supporting Docker:

1. **Build the Docker image**:
   ```bash
   docker build -t data-analysis-app .
   ```

2. **Run locally** (for testing):
   ```bash
   docker run -p 5000:5000 -e SECRET_KEY=your-secret-key data-analysis-app
   ```

3. **Deploy to cloud** (push to registry and deploy on your platform)

### 6. Docker Compose (Local Production)

```bash
# Set environment variables in .env file
echo "SECRET_KEY=your-very-secure-secret-key" > .env

# Start the application
docker-compose up -d

# View logs
docker-compose logs -f
```

### 7. Traditional VPS/Server

1. **Set up the server** (Ubuntu/CentOS):
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and dependencies
   sudo apt install python3 python3-pip nginx -y
   
   # Clone your repository
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   
   # Install Python dependencies
   pip3 install -r requirements.txt
   ```

2. **Configure Nginx** (create `/etc/nginx/sites-available/dataapp`):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. **Run with systemd** (create `/etc/systemd/system/dataapp.service`):
   ```ini
   [Unit]
   Description=Data Analysis Web App
   After=network.target
   
   [Service]
   User=www-data
   WorkingDirectory=/path/to/your/app
   Environment="FLASK_ENV=production"
   Environment="SECRET_KEY=your-very-secure-secret-key"
   ExecStart=/usr/local/bin/gunicorn wsgi:app
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

## Environment Variables

Set these environment variables on your deployment platform:

- `FLASK_ENV=production` (required)
- `SECRET_KEY=your-very-secure-secret-key` (required)
- `PORT=5000` (optional, some platforms set this automatically)

## Security Considerations

1. **Generate a secure SECRET_KEY**:
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

2. **Use HTTPS** in production (most platforms provide this automatically)

3. **Set proper file upload limits** (already configured in the app)

4. **Consider adding rate limiting** for production use

## Monitoring and Logs

- Most platforms provide built-in logging and monitoring
- Access logs through your platform's dashboard
- Monitor memory and CPU usage, especially during data processing

## Troubleshooting

### Common Issues:

1. **Memory limits**: Large datasets may require more memory
2. **File upload timeouts**: Adjust timeout settings for large files
3. **Missing dependencies**: Ensure all packages are in requirements.txt

### Solutions:

- Increase memory allocation on your platform
- Implement data streaming for large files
- Add comprehensive error handling and user feedback

## Cost Optimization

- **Free tiers available**: Heroku, Render, Railway offer free tiers
- **Pay-as-you-go**: Most platforms scale pricing with usage
- **Resource management**: Monitor and optimize based on actual usage

## Next Steps After Deployment

1. Test all functionality on the live site
2. Set up monitoring and alerts
3. Configure custom domain (if needed)
4. Set up CI/CD for automatic deployments
5. Consider adding user authentication for sensitive data
6. Implement data backup strategies

Choose the deployment method that best fits your needs and technical expertise!

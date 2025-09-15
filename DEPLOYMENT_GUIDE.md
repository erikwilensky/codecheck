# AI Code Assessment System - Deployment Guide

## PythonAnywhere Deployment with Custom Domain

### Prerequisites
- PythonAnywhere account (free or paid)
- Custom domain from Namecheap
- OpenAI API key

### Directory Structure
Your AI Code Assessment System will be deployed to:
```
/home/yourusername/ai-assessment-system/
```

This keeps it completely separate from your other webapp in:
```
/home/yourusername/oyco-data/
```

### Step 1: Prepare Your Local Project

1. **Create a deployment package:**
   ```bash
   # Create a clean deployment directory
   mkdir ai-assessment-deploy
   cd ai-assessment-deploy
   ```

2. **Copy essential files:**
   - `app/` directory (all Python code)
   - `static/` directory (HTML/CSS/JS files)
   - `requirements.txt`
   - `init_db.py`
   - `.env` file (create from env.example)

### Step 2: PythonAnywhere Setup

1. **Log into PythonAnywhere**
   - Go to [www.pythonanywhere.com](https://www.pythonanywhere.com)
   - Create account or log in

2. **Create a new web app:**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.9 or 3.10

3. **Create dedicated directory:**
   - Go to "Files" tab
   - Navigate to `/home/yourusername/`
   - Create new directory: `ai-assessment-system`
   - Upload your deployment files to this directory

### Step 3: Install Dependencies

1. **Open a Bash console** in PythonAnywhere
2. **Navigate to your project:**
   ```bash
   cd ~/ai-assessment-system
   ```

3. **Create virtual environment:**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.9 ai-assessment
   ```

4. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

### Step 4: Environment Configuration

1. **Create .env file:**
   ```bash
   nano .env
   ```

2. **Add your configuration:**
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=sqlite:///./ai_assessment.db
   ADMIN_PASSWORD=your_secure_admin_password
   ```

### Step 5: Database Setup

1. **Initialize the database:**
   ```bash
   python init_db.py
   ```

### Step 6: Web App Configuration

1. **Go to "Web" tab** in PythonAnywhere
2. **Edit the WSGI configuration file**
3. **Replace the content with:**

```python
import sys
import os

# Add your project directory to Python path
path = '/home/yourusername/ai-assessment-system'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['OPENAI_API_KEY'] = 'your_openai_api_key_here'
os.environ['DATABASE_URL'] = 'sqlite:///./ai_assessment.db'
os.environ['ADMIN_PASSWORD'] = 'your_secure_admin_password'

# Import your FastAPI app
from app.main import app

# For WSGI
application = app
```

### Step 7: Static Files Configuration

1. **In the "Web" tab**, configure static files:
   - URL: `/static/`
   - Directory: `/home/yourusername/ai-assessment-system/static/`

2. **Reload your web app**

### Step 8: Custom Domain Setup

#### A. Namecheap DNS Configuration

1. **Log into Namecheap**
2. **Go to your domain's DNS settings**
3. **Add these records:**

```
Type: A
Host: @
Value: 185.199.108.153
TTL: 30

Type: A
Host: @
Value: 185.199.109.153
TTL: 30

Type: A
Host: @
Value: 185.199.110.153
TTL: 30

Type: A
Host: @
Value: 185.199.111.153
TTL: 30
```

#### B. PythonAnywhere Domain Configuration

1. **In PythonAnywhere "Web" tab**
2. **Add your domain** to the "Domains" section
3. **Wait for DNS propagation** (can take up to 48 hours)

### Step 9: SSL Certificate

1. **In PythonAnywhere "Web" tab**
2. **Click "Add security"**
3. **Choose "Let's Encrypt"**
4. **Follow the prompts**

### Step 10: Testing

1. **Test your application:**
   - Visit your custom domain
   - Test the upload page: `yourdomain.com/upload`
   - Test the admin page: `yourdomain.com/admin`

2. **Check logs:**
   - Go to "Web" tab → "Log files"
   - Check for any errors

### Troubleshooting

#### Common Issues:

1. **Import errors:**
   - Check Python path in WSGI file
   - Ensure all dependencies are installed

2. **Database errors:**
   - Run `python init_db.py` again
   - Check file permissions

3. **Static files not loading:**
   - Verify static files configuration
   - Check file paths

4. **Domain not working:**
   - Wait for DNS propagation
   - Check DNS records
   - Verify domain is added to PythonAnywhere

#### Useful Commands:

```bash
# Check PythonAnywhere logs
tail -f /var/log/yourusername.pythonanywhere.com.error.log

# Restart web app
touch /var/www/yourusername_pythonanywhere_com_wsgi.py

# Check environment
echo $OPENAI_API_KEY

# Navigate to your project
cd ~/ai-assessment-system
```

### Security Considerations

1. **Use strong admin password**
2. **Keep API keys secure**
3. **Regular backups**
4. **Monitor logs for suspicious activity**

### Backup Strategy

1. **Database backup:**
   ```bash
   cp ai_assessment.db backup_$(date +%Y%m%d).db
   ```

2. **Code backup:**
   - Use Git for version control
   - Regular commits to repository

### Performance Optimization

1. **Enable caching** for static files
2. **Monitor resource usage**
3. **Consider paid plan** for better performance
4. **Optimize database queries**

### Support

- PythonAnywhere help: [help.pythonanywhere.com](https://help.pythonanywhere.com)
- FastAPI documentation: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- OpenAI API docs: [platform.openai.com/docs](https://platform.openai.com/docs) 
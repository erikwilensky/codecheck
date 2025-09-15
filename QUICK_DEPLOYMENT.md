# Quick Deployment Guide - AI Code Assessment System

## 🚀 Fast Deployment with Zip Upload

### What You Have
- ✅ `ai-assessment-system.zip` - Complete deployment package
- ✅ All files ready for PythonAnywhere

### Step 1: PythonAnywhere Setup

1. **Log into PythonAnywhere**
   - Go to [www.pythonanywhere.com](https://www.pythonanywhere.com)
   - Create account or log in

2. **Create a new web app:**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.9 or 3.10

### Step 2: Upload and Extract

1. **Go to "Files" tab** in PythonAnywhere
2. **Navigate to `/home/yourusername/`**
3. **Upload `ai-assessment-system.zip`**
4. **Open Bash console** and run:
   ```bash
   cd ~
   unzip ai-assessment-system.zip -d ai-assessment-system
   cd ai-assessment-system
   ```

### Step 3: Install Dependencies

```bash
# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.9 ai-assessment

# Install requirements
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Edit .env file with your real values
nano .env
```

Add your configuration:
```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./ai_assessment.db
ADMIN_PASSWORD=your_secure_admin_password
```

### Step 5: Initialize Database

```bash
python init_db.py
```

### Step 6: Configure Web App

1. **Go to "Web" tab** in PythonAnywhere
2. **Edit the WSGI configuration file**
3. **Replace content with:**

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

### Step 7: Configure Static Files

1. **In "Web" tab**, configure static files:
   - URL: `/static/`
   - Directory: `/home/yourusername/ai-assessment-system/static/`

2. **Reload your web app**

### Step 8: Test Your App

- Visit: `yourusername.pythonanywhere.com`
- Test upload: `yourusername.pythonanywhere.com/upload`
- Test admin: `yourusername.pythonanywhere.com/admin`

### Step 9: Custom Domain (Optional)

1. **Add your domain** to PythonAnywhere web app
2. **Configure DNS** in Namecheap (see NAMECHEAP_SETUP.md)
3. **Set up SSL certificate**

## 🎯 Quick Commands Summary

```bash
# Upload zip file to PythonAnywhere Files tab
# Then in Bash console:

cd ~
unzip ai-assessment-system.zip -d ai-assessment-system
cd ai-assessment-system
mkvirtualenv --python=/usr/bin/python3.9 ai-assessment
pip install -r requirements.txt
nano .env  # Add your API keys
python init_db.py
# Configure WSGI file in Web tab
# Set up static files
# Reload web app
```

## 📁 What's in the Zip

- `app/` - FastAPI application code
- `static/` - HTML/CSS/JS files
- `requirements.txt` - Python dependencies
- `init_db.py` - Database initialization
- `wsgi.py` - WSGI configuration
- `.env` - Environment template
- `DEPLOYMENT_INSTRUCTIONS.txt` - Detailed instructions

## 🔧 Troubleshooting

- **Import errors:** Check Python path in WSGI file
- **Database errors:** Run `python init_db.py` again
- **Static files not loading:** Verify static files configuration
- **Check logs:** Go to "Web" tab → "Log files"

## 🚀 Next Steps

1. Upload `ai-assessment-system.zip` to PythonAnywhere
2. Follow the commands above
3. Configure your custom domain
4. Test your application!

Your AI Code Assessment System will be live at:
`yourusername.pythonanywhere.com` 
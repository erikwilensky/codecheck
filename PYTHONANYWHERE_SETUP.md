# PythonAnywhere Deployment Guide

## Quick Setup for AI Code Assessment System

This guide will help you deploy the AI Code Assessment System to PythonAnywhere using the `pythonanywhere` branch.

### Prerequisites
- PythonAnywhere account with ASGI web app access
- Domain: `codecheck.website` (already configured)
- OpenAI API key

### Step 1: Clone the PythonAnywhere Branch

```bash
git clone -b pythonanywhere https://github.com/erikwilensky/codecheck.git
cd codecheck
```

### Step 2: Upload to PythonAnywhere

1. **Upload all files** to `/home/erikwilensky/code_share/` on PythonAnywhere
2. **Verify file structure:**
   ```
   /home/erikwilensky/code_share/
   ├── app/
   ├── static/
   ├── wsgi.py
   ├── requirements-pythonanywhere.txt
   ├── pythonanywhere_start.py
   └── pythonanywhere_config.py
   ```

### Step 3: Create New Web App

1. **Go to Web tab** in PythonAnywhere
2. **Click "Add a new async web app"**
3. **Choose "Manual configuration"**
4. **Select Python 3.9 or higher**
5. **Configure:**
   - **Source code:** `/home/erikwilensky/code_share`
   - **Working directory:** `/home/erikwilensky/code_share`

### Step 4: Configure WSGI

1. **Edit the WSGI file** (something like `/var/www/erikwilensky_pythonanywhere_com_wsgi.py`)
2. **Replace contents with:**
   ```python
   import sys
   import os
   
   # Add your project directory to Python path
   path = '/home/erikwilensky/code_share'
   if path not in sys.path:
       sys.path.append(path)
   
   # Set working directory
   os.chdir(path)
   
   # Set environment variables
   os.environ.setdefault('OPENAI_API_KEY', 'your_actual_openai_api_key')
   os.environ.setdefault('DATABASE_URL', 'sqlite:///./ai_assessment.db')
   os.environ.setdefault('ADMIN_PASSWORD', 'your_secure_admin_password')
   
   # Import your FastAPI app
   from app.main_pythonanywhere import app
   
   # For WSGI
   application = app
   ```

### Step 5: Install Dependencies

1. **Open Bash console** in PythonAnywhere
2. **Navigate to project:**
   ```bash
   cd /home/erikwilensky/code_share
   ```
3. **Install requirements:**
   ```bash
   pip install --user -r requirements-pythonanywhere.txt
   ```

### Step 6: Set Environment Variables

1. **In Web tab, go to "Environment variables"**
2. **Add these variables:**
   - `OPENAI_API_KEY`: Your actual OpenAI API key
   - `ADMIN_PASSWORD`: A secure password for admin access
   - `DATABASE_URL`: `sqlite:///./ai_assessment.db`

### Step 7: Initialize Database

1. **Run setup script:**
   ```bash
   cd /home/erikwilensky/code_share
   python pythonanywhere_start.py
   ```

### Step 8: Configure Domain

1. **In Web tab, go to "Domains"**
2. **Add domain:** `codecheck.website`
3. **Make sure it's enabled**

### Step 9: Reload Web App

1. **Click "Reload"** in the Web tab
2. **Check error log** if there are issues

### Step 10: Test Application

1. **Visit:** https://codecheck.website
2. **Test upload:** https://codecheck.website/upload
3. **Test admin:** https://codecheck.website/admin

## Key Features of PythonAnywhere Branch

### Optimized Files:
- `wsgi.py` - PythonAnywhere-specific WSGI configuration
- `app/main_pythonanywhere.py` - Optimized FastAPI app
- `requirements-pythonanywhere.txt` - Compatible dependencies
- `pythonanywhere_start.py` - Setup and initialization script
- `pythonanywhere_config.py` - Configuration management

### Improvements:
- ✅ **Path handling** - Proper Python path management
- ✅ **CORS settings** - PythonAnywhere-specific origins
- ✅ **Database initialization** - Automatic setup
- ✅ **Error handling** - Better error messages
- ✅ **Logging** - Startup and shutdown events
- ✅ **Static files** - Proper static file serving

## Troubleshooting

### Common Issues:

1. **Import errors:**
   - Check that all files are uploaded correctly
   - Verify the path in wsgi.py matches your actual path

2. **Database errors:**
   - Run `python pythonanywhere_start.py` again
   - Check file permissions

3. **Environment variable issues:**
   - Verify all environment variables are set
   - Reload the web app after changing variables

4. **Static files not loading:**
   - Ensure static directory exists
   - Check file permissions

### Error Logs:
- Check the error log in the Web tab
- Common location: `/var/log/erikwilensky.pythonanywhere.com.error.log`

## Security Notes

1. **Never commit API keys** to version control
2. **Use strong passwords** for admin access
3. **HTTPS is provided** automatically by PythonAnywhere
4. **Regularly update** your dependencies

## Maintenance

1. **Regular backups:** Download your database file periodically
2. **Updates:** Keep dependencies updated
3. **Monitoring:** Check error logs regularly

## Support

If you encounter issues:
1. Check PythonAnywhere error logs
2. Verify environment variables are set
3. Ensure all dependencies are installed
4. Test locally before deploying changes

---

**Ready to deploy?** Follow the steps above and your AI Code Assessment System will be live on PythonAnywhere! 🚀

# PythonAnywhere Deployment Guide for AI Code Assessment System

## Prerequisites
- PythonAnywhere account with ASGI web app access enabled
- Domain: codecheck.website (already configured)
- OpenAI API key
- **Multiple web apps supported** - This will be a separate web app

## Understanding Multiple Web Apps

**Your PythonAnywhere account can have multiple web apps running simultaneously:**

- ✅ **Separate directories** - Each web app has its own folder
- ✅ **Independent configurations** - Each has its own WSGI file
- ✅ **Different domains** - Each can have its own domain
- ✅ **No conflicts** - They don't interfere with each other

**Example structure:**
```
/home/yourusername/
├── code_share/                    # AI Assessment System
├── your_other_webapp/            # Existing web app
└── another_webapp/               # Another existing web app
```

## Step 1: Upload Your Code

1. **Upload your project files to PythonAnywhere:**
   - Use the Files tab in PythonAnywhere
   - Upload all files from your `code_share` directory
   - Place them in `/home/yourusername/code_share/`

2. **Verify file structure:**
   ```
   /home/yourusername/code_share/
   ├── app/
   ├── static/
   ├── requirements.txt
   ├── wsgi.py
   ├── pythonanywhere_setup.py
   └── ...
   ```

## Step 2: Configure Your NEW Web App

1. **Go to Web tab in PythonAnywhere**

2. **Create a new web app (separate from existing ones):**
   - Click "Add a new async web app"
   - Choose "Manual configuration"
   - Select Python 3.9 or higher
   - **This creates a completely new async web app for FastAPI**

3. **Configure the NEW web app:**
   - **Source code:** `/home/yourusername/code_share`
   - **Working directory:** `/home/yourusername/code_share`
   - **WSGI configuration file:** Will be something like `/var/www/yourusername_pythonanywhere_com_wsgi.py`

4. **Edit the WSGI file for THIS web app:**
   Replace the contents with:
   ```python
   import sys
   import os
   
   # Add your project directory to Python path
   path = '/home/yourusername/code_share'
   if path not in sys.path:
       sys.path.append(path)
   
   # Set environment variables
   os.environ['OPENAI_API_KEY'] = 'your_actual_openai_api_key'
   os.environ['DATABASE_URL'] = 'sqlite:///./ai_assessment.db'
   os.environ['ADMIN_PASSWORD'] = 'your_secure_admin_password'
   
   # Import your FastAPI app
   from app.main import app
   
   # For WSGI
   application = app
   ```

## Step 3: Install Dependencies

1. **Open a Bash console in PythonAnywhere**

2. **Navigate to your project:**
   ```bash
   cd /home/yourusername/code_share
   ```

3. **Install requirements:**
   ```bash
   pip install --user -r requirements.txt
   ```

## Step 4: Set Up Environment Variables

1. **In the Web tab, go to "Environment variables"**

2. **Add these variables for THIS web app:**
   - `OPENAI_API_KEY`: Your actual OpenAI API key
   - `ADMIN_PASSWORD`: A secure password for admin access
   - `DATABASE_URL`: `sqlite:///./ai_assessment.db`

## Step 5: Initialize the Database

1. **Run the setup script:**
   ```bash
   cd /home/yourusername/code_share
   python pythonanywhere_setup.py
   ```

## Step 6: Configure Your Domain

1. **In the Web tab, go to "Domains"**

2. **Add your domain:**
   - Add `codecheck.website`
   - Make sure it's enabled
   - **This domain will be specific to this web app**

## Step 7: Reload Your Web App

1. **Click "Reload" in the Web tab**
   - This reloads only THIS web app
   - Your other web apps remain unaffected

2. **Check the error log if there are issues**

## Step 8: Test Your Application

1. **Visit your domain:** https://codecheck.website
2. **Test the upload page:** https://codecheck.website/upload
3. **Test the admin panel:** https://codecheck.website/admin

## Managing Multiple Web Apps

### In the Web Tab, you'll see:
- **Web app 1:** Your existing web app (unchanged)
- **Web app 2:** Your existing web app (unchanged)
- **Web app 3:** AI Code Assessment System (new)
  - Domain: `codecheck.website`
  - Source: `/home/yourusername/code_share`
  - Status: Running

### Each web app has:
- ✅ **Independent configuration**
- ✅ **Separate error logs**
- ✅ **Different domains**
- ✅ **Own environment variables**

## Troubleshooting

### Common Issues:

1. **Import errors:**
   - Check that all files are uploaded correctly
   - Verify the path in wsgi.py matches your actual path

2. **Database errors:**
   - Run the setup script again
   - Check file permissions

3. **Environment variable issues:**
   - Verify all environment variables are set in PythonAnywhere
   - Reload the web app after changing environment variables

4. **Static files not loading:**
   - Make sure the static directory exists
   - Check file permissions

### Error Logs:
- Check the error log in the Web tab for specific error messages
- Common locations for logs: `/var/log/yourusername.pythonanywhere.com.error.log`

## Security Notes

1. **Never commit API keys to version control**
2. **Use strong passwords for admin access**
3. **Consider using HTTPS (PythonAnywhere provides this automatically)**
4. **Regularly update your dependencies**

## Maintenance

1. **Regular backups:** Download your database file periodically
2. **Updates:** Keep your dependencies updated
3. **Monitoring:** Check error logs regularly

## Support

If you encounter issues:
1. Check the PythonAnywhere error logs
2. Verify all environment variables are set
3. Ensure all dependencies are installed
4. Test locally before deploying changes 
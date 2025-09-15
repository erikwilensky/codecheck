# PythonAnywhere ASGI Deployment Guide for AI Code Assessment System

## Overview

PythonAnywhere now supports ASGI (Asynchronous Server Gateway Interface) deployment, which is perfect for FastAPI applications. This is the recommended approach for your AI Code Assessment System.

## Prerequisites

- PythonAnywhere account
- Domain: codecheck.website (already configured)
- OpenAI API key
- API token (generated from PythonAnywhere)

## Step 1: Install Command Line Tools

1. **Open a Bash console in PythonAnywhere**

2. **Install the PythonAnywhere CLI tool:**
   ```bash
   pip install --upgrade pythonanywhere
   ```

3. **Verify installation:**
   ```bash
   pa --help
   ```

## Step 2: Create Virtual Environment

1. **Create a virtual environment:**
   ```bash
   mkvirtualenv code_share_env --python=python3.10
   ```

2. **Activate the environment:**
   ```bash
   workon code_share_env
   ```

3. **Install dependencies:**
   ```bash
   pip install "uvicorn[standard]" fastapi sqlalchemy openai python-dotenv python-multipart fpdf2 pydantic python-jose[cryptography] passlib[bcrypt]
   ```

## Step 3: Upload Your Code

1. **Upload your project files:**
   - Use the Files tab to upload your `code_share` directory
   - Or use the zip file method from the previous guide

2. **Verify your code is in place:**
   ```bash
   cd ~/code_share
   ls -la
   ```

## Step 4: Create the ASGI Website

1. **Create the website using the pa command:**
   ```bash
   pa website create --domain codecheck.website --command '/home/YOURUSERNAME/.virtualenvs/code_share_env/bin/uvicorn --app-dir /home/YOURUSERNAME/code_share --uds ${DOMAIN_SOCKET} app.main:app'
   ```

   **Replace YOURUSERNAME with your actual PythonAnywhere username**

2. **You should see:**
   ```
   < All done! Your site is now live at codecheck.website. >
      \
       ~<:>>>>>>>>>>
   ```

## Step 5: Set Environment Variables

1. **Create a .env file in your project:**
   ```bash
   cd ~/code_share
   nano .env
   ```

2. **Add your environment variables:**
   ```
   OPENAI_API_KEY=your_actual_openai_api_key
   DATABASE_URL=sqlite:///./ai_assessment.db
   ADMIN_PASSWORD=your_secure_admin_password
   ```

## Step 6: Initialize Database

1. **Run the setup script:**
   ```bash
   cd ~/code_share
   python pythonanywhere_setup.py
   ```

## Step 7: Reload Your Website

1. **Reload to apply changes:**
   ```bash
   pa website reload --domain codecheck.website
   ```

2. **You should see:**
   ```
   < Website codecheck.website has been reloaded! >
      \
       ~<:>>>>>>>>>>
   ```

## Step 8: Test Your Application

1. **Visit your domain:** https://codecheck.website
2. **Test endpoints:**
   - Root: https://codecheck.website/
   - Status: https://codecheck.website/status
   - Upload: https://codecheck.website/upload
   - Admin: https://codecheck.website/admin

## Managing Your ASGI Website

### Check Website Status
```bash
pa website get --domain codecheck.website
```

### List All Websites
```bash
pa website get
```

### Reload After Code Changes
```bash
pa website reload --domain codecheck.website
```

### Delete Website (if needed)
```bash
pa website delete --domain codecheck.website
```

## Logs and Debugging

### Error Log
```bash
tail -f /var/log/codecheck.website.error.log
```

### Server Log
```bash
tail -f /var/log/codecheck.website.server.log
```

### Access Log
```bash
tail -f /var/log/codecheck.website.access.log
```

## Troubleshooting

### Common Issues:

1. **Import errors:**
   - Check that all files are uploaded correctly
   - Verify the virtual environment is activated
   - Ensure all dependencies are installed

2. **Environment variable issues:**
   - Make sure .env file exists in project directory
   - Check that variables are set correctly

3. **Database errors:**
   - Run the setup script again
   - Check file permissions

4. **Website not loading:**
   - Check the error logs
   - Verify the command syntax is correct
   - Make sure the domain is configured properly

## Command Breakdown

The deployment command:
```bash
/home/YOURUSERNAME/.virtualenvs/code_share_env/bin/uvicorn --app-dir /home/YOURUSERNAME/code_share --uds ${DOMAIN_SOCKET} app.main:app
```

**What each part does:**
- `/home/YOURUSERNAME/.virtualenvs/code_share_env/bin/uvicorn` - Path to uvicorn in your virtual environment
- `--app-dir /home/YOURUSERNAME/code_share` - Directory containing your code
- `--uds ${DOMAIN_SOCKET}` - Unix domain socket for communication
- `app.main:app` - Import the `app` object from `app.main` module

## Advantages of ASGI Deployment

- ✅ **Better performance** - Native async support
- ✅ **Proper FastAPI compatibility** - Designed for async frameworks
- ✅ **WebSocket support** - If needed for real-time features
- ✅ **Modern deployment** - Uses the latest PythonAnywhere features
- ✅ **Simpler configuration** - No WSGI file needed

## Security Notes

1. **Keep your API keys secure** - Never commit them to version control
2. **Use strong passwords** - For admin access
3. **Monitor logs regularly** - Check for any issues
4. **Backup your database** - Download periodically

## Next Steps

1. **Test all functionality** - Upload, analysis, admin panel
2. **Monitor performance** - Check logs for any issues
3. **Set up monitoring** - Regular health checks
4. **Plan for scaling** - Consider database upgrades if needed 
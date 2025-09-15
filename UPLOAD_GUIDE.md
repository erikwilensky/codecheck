# PythonAnywhere File Upload Guide

## Multiple Web Apps on PythonAnywhere

**Yes, this will be in its own directory!** Each web app on PythonAnywhere is completely separate:

- ✅ **Separate directories** - Your AI assessment system will be in `/home/yourusername/code_share/`
- ✅ **Independent configuration** - Has its own WSGI file and settings
- ✅ **No interference** - Won't affect your other web apps
- ✅ **Separate domains** - Will use `codecheck.website` specifically

## Method 1: Using PythonAnywhere Console (Recommended)

### Step 1: Create a Zip File Locally

1. **Select your files:**
   - Open your `code_share` folder
   - Select all files and folders (Ctrl+A)
   - Right-click and choose "Send to" → "Compressed (zipped) folder"
   - Name it `code_share.zip`

2. **Verify the zip contains:**
   ```
   code_share.zip
   ├── app/
   ├── static/
   ├── requirements.txt
   ├── wsgi.py
   ├── pythonanywhere_setup.py
   └── ... (all other files)
   ```

### Step 2: Upload to PythonAnywhere

1. **Go to PythonAnywhere Dashboard**
   - Log in to your PythonAnywhere account
   - Click on "Files" tab

2. **Upload the zip file:**
   - Click "Upload a file"
   - Select your `code_share.zip` file
   - Wait for upload to complete

3. **Open a Bash console:**
   - Click on "Consoles" tab
   - Click "Bash" to open a new console

### Step 3: Extract and Organize Files

1. **Navigate to your home directory:**
   ```bash
   cd ~
   ```

2. **List files to confirm upload:**
   ```bash
   ls -la
   ```
   You should see `code_share.zip`

3. **Create the project directory (if it doesn't exist):**
   ```bash
   mkdir -p code_share
   ```

4. **Extract the zip file:**
   ```bash
   unzip code_share.zip -d code_share/
   ```

5. **Verify the extraction:**
   ```bash
   ls -la code_share/
   ```

6. **Check the structure:**
   ```bash
   find code_share/ -type f | head -10
   ```

7. **Verify key directories exist:**
   ```bash
   ls -la code_share/app/
   ls -la code_share/static/
   ```

### Step 4: Create New Web App (Separate from Others)

1. **Go to Web tab in PythonAnywhere**

2. **Create new web app:**
   - Click "Add a new async web app"
   - Choose "Manual configuration"
   - Select Python 3.9 or higher
   - **This creates a completely separate async web app for FastAPI**

3. **Configure paths for THIS web app:**
   - **Source code:** `/home/yourusername/code_share`
   - **Working directory:** `/home/yourusername/code_share`
   - **WSGI configuration file:** Will be something like `/var/www/yourusername_pythonanywhere_com_wsgi.py`

4. **Edit the WSGI file for THIS web app:**
   - Click on the WSGI configuration file link
   - Replace contents with:
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

## Directory Structure on PythonAnywhere

After setup, your PythonAnywhere account will have:

```
/home/yourusername/
├── code_share/                    # Your AI assessment system
│   ├── app/
│   ├── static/
│   ├── requirements.txt
│   └── ...
├── your_other_webapp/            # Your existing web apps
│   └── ...
└── another_webapp/               # Another existing web app
    └── ...
```

## Web Apps Configuration

In the Web tab, you'll see multiple web apps:

- **Web app 1:** Your existing web app (unchanged)
- **Web app 2:** Your existing web app (unchanged)
- **Web app 3:** AI Code Assessment System (new)
  - Domain: `codecheck.website`
  - Source: `/home/yourusername/code_share`
  - WSGI: `/var/www/yourusername_pythonanywhere_com_wsgi.py`

## Method 2: Using Git (Alternative)

If you have your code in a Git repository:

1. **Open Bash console in PythonAnywhere**

2. **Clone your repository:**
   ```bash
   cd ~
   git clone https://github.com/yourusername/code_share.git
   ```

3. **Follow the same web app configuration steps**

## Method 3: Manual File Upload

1. **Go to Files tab in PythonAnywhere**

2. **Create directory structure:**
   - Click "New directory" → name it `code_share`
   - Navigate into `code_share`
   - Create subdirectories: `app`, `static`

3. **Upload files individually:**
   - Upload each file to the appropriate directory
   - This is more time-consuming but gives you control

## Console Commands for Verification

After uploading, run these commands to verify everything is correct:

```bash
# Navigate to your project
cd ~/code_share

# Check file structure
ls -la

# Check if all directories exist
ls -la app/
ls -la static/

# Check if key files exist
ls -la requirements.txt wsgi.py pythonanywhere_setup.py

# Check Python can import your app
python -c "import app.main; print('✅ App imports successfully')"

# Run setup script
python pythonanywhere_setup.py
```

## Troubleshooting Upload Issues

### Common Problems:

1. **Zip file too large:**
   - Remove unnecessary files (like `__pycache__`, `.git`)
   - Create a smaller zip with only essential files

2. **Permission errors:**
   ```bash
   chmod -R 755 ~/code_share
   ```

3. **Missing files:**
   - Check if all files uploaded correctly
   - Re-upload missing files individually

4. **Import errors:**
   - Verify the path in wsgi.py matches your actual path
   - Check that all `__init__.py` files exist

## Quick Verification Checklist

After upload, verify:
- [ ] All files are in `/home/yourusername/code_share/`
- [ ] `app/` directory contains all Python files
- [ ] `static/` directory contains HTML files
- [ ] `requirements.txt` exists
- [ ] `wsgi.py` exists and is configured
- [ ] `pythonanywhere_setup.py` exists

## Next Steps After Upload

1. **Install dependencies:**
   ```bash
   cd ~/code_share
   pip install --user -r requirements.txt
   ```

2. **Set environment variables** in Web tab

3. **Run setup script:**
   ```bash
   python pythonanywhere_setup.py
   ```

4. **Reload your web app**

5. **Test your domain:** https://codecheck.website 
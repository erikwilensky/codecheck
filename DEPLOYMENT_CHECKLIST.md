# PythonAnywhere Deployment Checklist

## ✅ Pre-Deployment
- [ ] OpenAI API key ready
- [ ] PythonAnywhere account with ASGI access enabled
- [ ] Domain codecheck.website configured
- [ ] All project files ready for upload

## ✅ Upload Files
- [ ] Upload all files to `/home/yourusername/code_share/`
- [ ] Verify file structure is correct
- [ ] Check that static/ directory exists

## ✅ Web App Configuration
- [ ] Create new web app (Manual configuration)
- [ ] Set source code to `/home/yourusername/code_share`
- [ ] Set working directory to `/home/yourusername/code_share`
- [ ] Configure WSGI file with correct paths

## ✅ Environment Variables
- [ ] Set OPENAI_API_KEY
- [ ] Set ADMIN_PASSWORD
- [ ] Set DATABASE_URL (sqlite:///./ai_assessment.db)

## ✅ Dependencies
- [ ] Install requirements: `pip install --user -r requirements.txt`
- [ ] Verify all packages installed successfully

## ✅ Database Setup
- [ ] Run setup script: `python pythonanywhere_setup.py`
- [ ] Verify database created successfully

## ✅ Domain Configuration
- [ ] Add codecheck.website to domains
- [ ] Enable the domain

## ✅ Test Deployment
- [ ] Reload web app
- [ ] Test root endpoint: https://codecheck.website/
- [ ] Test status endpoint: https://codecheck.website/status
- [ ] Test upload page: https://codecheck.website/upload
- [ ] Test admin panel: https://codecheck.website/admin

## ✅ Post-Deployment
- [ ] Check error logs for any issues
- [ ] Test file upload functionality
- [ ] Test AI analysis features
- [ ] Verify admin access works

## 🔧 Troubleshooting
- [ ] Check PythonAnywhere error logs
- [ ] Verify environment variables are set
- [ ] Ensure all dependencies are installed
- [ ] Check file permissions

## 📝 Notes
- Remember to replace `yourusername` with your actual PythonAnywhere username
- Keep your API keys secure
- Monitor error logs regularly
- Backup database periodically 
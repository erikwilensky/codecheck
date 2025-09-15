# 🚀 Deployment Guide - Privacy-First System

This guide will help you deploy the AI Code Assessment System with **privacy-focused** student identification using anonymous IDs.

## 🎯 **System Overview**

The system supports **direct file uploads** with anonymous student IDs, making it perfect for school environments with strict privacy requirements.

### **Features:**
- ✅ Direct file upload via web interface
- ✅ **Privacy-focused** using student IDs (no personal data)
- ✅ AI-powered code analysis using OpenAI
- ✅ Personalized quiz generation
- ✅ Historical submission tracking
- ✅ Works behind school firewalls
- ✅ No external dependencies (except OpenAI API)

## 🆔 **Student ID System**

### **Privacy-First Approach:**
- **No personal information** collected (names, emails, etc.)
- **Student IDs** assigned by teachers (e.g., CS101001, CS101002)
- **Class codes** for organization (e.g., CS101, MATH202)
- **Anonymous tracking** of learning progress

### **For Teachers:**
```bash
# Generate student IDs for your class
python tools/generate_student_ids.py

# This will create files like:
# - student_ids_CS101_20241201.txt
# - all_student_ids_20241201.txt
```

### **Example Student IDs:**
- CS101001, CS101002, CS101003... (CS101 class)
- MATH202001, MATH202002... (MATH202 class)
- PHYS101001, PHYS101002... (PHYS101 class)

## 🏗️ **Deployment Options**

### **Option 1: Cloud Hosting (Recommended)**

#### **A. Railway (Free Tier Available)**
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login to Railway
railway login

# 3. Initialize project
railway init

# 4. Set environment variables
railway variables set OPENAI_API_KEY=your_openai_key
railway variables set DATABASE_URL=postgresql://...

# 5. Deploy
railway up
```

#### **B. Render (Free Tier Available)**
```bash
# 1. Connect your GitHub repository
# 2. Set environment variables in Render dashboard
# 3. Deploy automatically
```

#### **C. Heroku**
```bash
# 1. Install Heroku CLI
# 2. Create Procfile
echo "web: uvicorn backend.app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# 3. Deploy
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_openai_key
git push heroku main
```

### **Option 2: VPS Hosting**

#### **Ubuntu/Debian Server Setup:**
```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# 3. Clone your repository
git clone https://github.com/yourusername/code_share.git
cd code_share

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies
pip install -r backend/requirements.txt

# 6. Set up environment variables
cp backend/env.example backend/.env
# Edit .env with your OpenAI API key

# 7. Initialize database
cd backend
python setup.py

# 8. Run with Gunicorn
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🔧 **Environment Setup**

### **Required Environment Variables:**
```bash
# OpenAI API (Required)
OPENAI_API_KEY=sk-your-openai-api-key

# Database (Optional - defaults to SQLite)
DATABASE_URL=sqlite:///./ai_assessment.db

# Server Settings (Optional)
HOST=0.0.0.0
PORT=8000
```

### **Getting OpenAI API Key:**
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create account or sign in
3. Go to API Keys section
4. Create new API key
5. Copy and save securely

## 📋 **Quick Start (Local Testing)**

### **1. Setup Environment:**
```bash
# Navigate to backend
cd backend

# Copy environment template
cp env.example .env

# Edit .env with your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### **2. Install Dependencies:**
```bash
pip install -r requirements.txt
```

### **3. Initialize Database:**
```bash
python setup.py
```

### **4. Start Server:**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **5. Test the System:**
```bash
# Run test script
python tests/test_upload.py

# Or visit in browser:
# http://localhost:8000/upload
```

## 🌐 **Access Points**

Once deployed, your system will have these endpoints:

- **📝 Upload Interface:** `https://your-domain.com/upload`
- **🔍 API Documentation:** `https://your-domain.com/docs`
- **📊 Health Check:** `https://your-domain.com/health`

## 🎓 **Student Usage**

### **For Students:**
1. Get assigned student ID from teacher
2. Visit the upload page
3. Enter student ID and class code
4. Select code files
5. Add a commit message
6. Submit and get instant analysis + quiz

### **For Teachers:**
1. Generate student IDs using the provided tool
2. Distribute IDs to students
3. Access API endpoints to view submissions by ID
4. Monitor student progress anonymously
5. Review AI-generated quizzes
6. Track learning patterns without personal data

## 🔒 **Security Considerations**

### **Production Security:**
```bash
# 1. Use HTTPS (required for production)
# 2. Set up proper CORS
# 3. Add rate limiting
# 4. Validate file uploads
# 5. Secure environment variables
```

### **Environment Variables Security:**
- Never commit `.env` files
- Use secure secret management
- Rotate API keys regularly
- Monitor API usage

## 📊 **Monitoring & Maintenance**

### **Health Checks:**
```bash
# Check if system is running
curl https://your-domain.com/health

# Check API documentation
curl https://your-domain.com/docs
```

### **Database Backup:**
```bash
# Backup SQLite database
cp ai_assessment.db backup_$(date +%Y%m%d).db

# For PostgreSQL
pg_dump your_database > backup.sql
```

## 🚨 **Troubleshooting**

### **Common Issues:**

1. **Import Errors:**
   ```bash
   # Make sure you're in the right directory
   cd backend
   python -m uvicorn app.main:app --reload
   ```

2. **OpenAI API Errors:**
   - Check API key is correct
   - Verify account has credits
   - Check rate limits

3. **Database Errors:**
   ```bash
   # Reinitialize database
   python setup.py
   ```

4. **Port Already in Use:**
   ```bash
   # Use different port
   python -m uvicorn app.main:app --port 8001
   ```

## 📈 **Scaling Considerations**

### **For Large Classes:**
- Use PostgreSQL instead of SQLite
- Implement caching (Redis)
- Add load balancing
- Monitor OpenAI API costs

### **Cost Optimization:**
- Set OpenAI API usage limits
- Implement request throttling
- Cache analysis results
- Monitor usage patterns

## 🎯 **Next Steps**

1. **Deploy to your chosen platform**
2. **Test with a small group of students**
3. **Monitor performance and costs**
4. **Gather feedback and iterate**
5. **Scale up as needed**

## 📞 **Support**

If you encounter issues:
1. Check the troubleshooting section
2. Review the API documentation at `/docs`
3. Check the logs for error messages
4. Test with the provided test scripts

---

**🎉 You're ready to deploy your privacy-focused AI Code Assessment System!** 
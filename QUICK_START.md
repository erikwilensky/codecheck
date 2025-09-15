# 🚀 Quick Start Guide

## ⚠️ **If Everything is Hanging**

The hanging issue is caused by a background server process. Here's how to fix it:

### **Step 1: Stop the Background Server**
1. **Press `Ctrl + C`** in your terminal
2. **Or close your terminal** and open a new one
3. **Or restart your computer** if needed

### **Step 2: Test the System (No Server Required)**
```bash
cd backend
python test_system.py
```

This will test everything without starting a server.

### **Step 3: Start Server on Different Port**
```bash
python start_server.py
```

This starts the server on port 8001 instead of 8000.

## 🔧 **Quick Setup**

### **1. Test System (No Server)**
```bash
cd backend
python test_system.py
```

### **2. Setup Environment**
```bash
# Copy environment template
cp env.example .env

# Edit .env with your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Initialize Database**
```bash
python setup.py
```

### **5. Start Server (Port 8001)**
```bash
python start_server.py
```

### **6. Access the System**
- **Upload Page:** http://localhost:8001/upload
- **API Docs:** http://localhost:8001/docs
- **Health Check:** http://localhost:8001/health

## 🆔 **Generate Student IDs**
```bash
python generate_student_ids.py
```

## 🧪 **Test Upload**
```bash
python test_upload.py
```

## 🎯 **What to Do Next**

1. **If tests pass:** System is ready to use
2. **If tests fail:** Check the error messages
3. **If server won't start:** Try the different port (8001)
4. **If still hanging:** Restart your computer

## 📞 **Troubleshooting**

### **Server Won't Start:**
- Try port 8001: `python start_server.py`
- Check if port is in use: `netstat -ano | findstr :8001`
- Kill processes: `taskkill /f /im python.exe`

### **Import Errors:**
- Make sure you're in the `backend` directory
- Install requirements: `pip install -r requirements.txt`
- Check Python path: `python -c "import sys; print(sys.path)"`

### **Database Errors:**
- Run setup: `python setup.py`
- Check file permissions
- Delete database file and recreate: `rm ai_assessment.db`

---

**🎉 Once working, you'll have a privacy-focused code assessment system!** 
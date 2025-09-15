# AI Code Assessment System

A privacy-focused AI-powered code assessment system for educational institutions.

## 🎯 Features

- **📝 Single File Upload** - Students upload one code file per assignment
- **🆔 Anonymous Student IDs** - Privacy-focused identification system
- **📋 Teacher-Created Assignments** - Predefined assignment list with custom options
- **🤖 AI Code Analysis** - Automated code review and feedback
- **📊 Personalized Quizzes** - AI-generated quizzes based on code analysis
- **🔒 Privacy Compliant** - No personal data collection (FERPA/GDPR ready)
- **🌐 Web Interface** - Simple, clean upload portal

## 🚀 Quick Start

### 1. Test the System
```bash
python test.py
```

### 2. Start the Server
```bash
python start.py
```

### 3. Access the System
- **Upload Page:** http://127.0.0.1:8000/upload
- **API Docs:** http://127.0.0.1:8000/docs

## 📁 Project Structure

```
code_share/
├── app/                    # Main application
│   ├── api/               # API endpoints
│   ├── models/            # Database models
│   ├── services/          # Business logic
│   └── main.py           # FastAPI app
├── static/                # Web interface files
├── docs/                  # Documentation
├── start.py              # Server startup script
├── test.py               # System test script
├── generate_student_ids.py # Student ID generator
├── requirements.txt       # Python dependencies
└── env.example           # Environment template
```

## 🆔 Student ID System

### Privacy-Focused Design
- **Student IDs:** STU001, STU002, etc.
- **No Personal Data:** Anonymous identification only
- **Teacher Control:** You create and distribute student IDs

### Generate Student IDs
```bash
python generate_student_ids.py
```

## 📋 Assignment System

### Predefined Assignments
- Python Calculator
- Data Structures
- Web Scraper
- Database Design
- Algorithm Implementation
- Object-Oriented Design
- API Development
- Testing Framework
- Custom assignments (teacher-defined)

### How It Works
1. **Teacher creates assignments** - Students select from dropdown
2. **Single file upload** - One code file per submission
3. **AI analysis** - Automated code review
4. **Personalized quiz** - Generated based on code analysis

## 🔧 Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Setup
```bash
# Copy environment template
copy env.example .env

# Edit .env file with your API keys
# OPENAI_API_KEY=your-api-key-here
```

### 3. Database Setup
The system automatically creates the SQLite database on first run.

## 📋 Usage

### For Students
1. Visit http://127.0.0.1:8000/upload
2. Enter your Student ID
3. Select an assignment from the dropdown
4. Upload your code file
5. Receive AI analysis and personalized quiz

### For Teachers
1. Generate student IDs: `python generate_student_ids.py`
2. Distribute IDs to students
3. Monitor submissions through the API
4. Create custom assignments as needed

## 🔒 Privacy & Compliance

- **No Personal Data:** Only anonymous student IDs
- **FERPA Compliant:** No student names, emails, or personal info
- **GDPR Ready:** Minimal data collection
- **Local Storage:** All data stored locally by default

## 🛠️ Development

### Run Tests
```bash
python test.py
```

### Start Development Server
```bash
python start.py
```

### API Documentation
Visit http://127.0.0.1:8000/docs for interactive API documentation.

## 📚 API Endpoints

- `POST /api/upload/code` - Upload single code file
- `GET /api/upload/submissions/{student_id}` - Get student submissions
- `GET /api/upload/students` - List all students
- `GET /health` - Health check

## 🚀 Deployment

### Local Development
```bash
python start.py
```

### Production Deployment
1. Set up environment variables
2. Use a production WSGI server
3. Configure database (PostgreSQL recommended)
4. Set up reverse proxy (nginx)

## 📄 License

This project is designed for educational use.

## 🤝 Contributing

1. Test the system: `python test.py`
2. Make changes
3. Test again: `python test.py`
4. Submit pull request

---

**🎉 Your privacy-focused AI code assessment system is ready!** 
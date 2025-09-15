# 📊 API Reference - Privacy-First System

## 🎯 **Overview**

This document provides comprehensive API documentation for the AI Code Assessment System with privacy-focused student identification.

## 🔗 **Base URL**

- **Local Development:** `http://localhost:8000`
- **Production:** `https://your-domain.com`

## 🔐 **Authentication**

Currently, the system uses **anonymous student IDs** for identification. No authentication tokens are required.

## 📋 **API Endpoints**

### **🌐 Core Endpoints**

#### **Health Check**
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "services": "running"
}
```

#### **API Documentation**
```http
GET /docs
```

**Response:** Swagger UI interface

#### **Upload Page**
```http
GET /upload
```

**Response:** HTML upload form

### **📝 Upload Endpoints**

#### **Upload Code Submission**
```http
POST /api/upload/code
Content-Type: multipart/form-data
```

**Form Data:**
- `student_id` (string, required): Student ID (e.g., "CS101015")
- `class_code` (string, required): Class code (e.g., "CS101")
- `assignment_name` (string, required): Assignment name
- `commit_message` (string, required): Description of changes
- `files` (file[], required): Code files to upload

**Response:**
```json
{
  "success": true,
  "submission_id": 1,
  "analysis_id": 1,
  "quiz_id": 1,
  "message": "Code submission uploaded and analyzed successfully"
}
```

**Error Response:**
```json
{
  "detail": "Upload failed: [error message]"
}
```

#### **Get Student Submissions**
```http
GET /api/upload/submissions/{student_id}
```

**Parameters:**
- `student_id` (integer): Database student ID

**Response:**
```json
{
  "student_id": 1,
  "submissions": [
    {
      "id": 1,
      "assignment": "Python Calculator",
      "commit_message": "Implemented basic calculator",
      "files_changed": ["calculator.py", "README.md"],
      "lines_added": 150,
      "created_at": "2024-12-01T10:30:00"
    }
  ]
}
```

#### **Get All Students**
```http
GET /api/upload/students
```

**Response:**
```json
{
  "students": [
    {
      "id": 1,
      "student_id": "CS101015",
      "class_code": "CS101",
      "created_at": "2024-12-01T10:30:00"
    }
  ]
}
```

### **🔍 Analysis Endpoints**

#### **Get Analysis by ID**
```http
GET /api/analyses/{analysis_id}
```

**Response:**
```json
{
  "id": 1,
  "student_id": 1,
  "submission_id": 1,
  "historical_analysis": {
    "learning_trajectory": "gradual",
    "consistency_score": 0.85,
    "improvement_rate": 0.12,
    "pattern_anomalies": []
  },
  "tool_dependency": {
    "ai_usage_probability": 0.15,
    "copilot_usage_probability": 0.05,
    "copy_paste_probability": 0.02,
    "confidence": 0.78
  },
  "learning_progression": {
    "overall_progression": "positive",
    "skill_development_rate": 0.08,
    "understanding_level": "intermediate"
  },
  "authentic_learning_assessment": {
    "authentic_learning_score": 0.82,
    "genuine_understanding": true,
    "gradual_improvement": true,
    "consistent_approach": true
  },
  "intervention_recommendations": {
    "intervention_needed": false,
    "intervention_type": "none",
    "specific_recommendations": [],
    "priority": "low"
  },
  "created_at": "2024-12-01T10:30:00"
}
```

#### **Get All Analyses**
```http
GET /api/analyses
```

**Response:**
```json
{
  "analyses": [
    {
      "id": 1,
      "student_id": 1,
      "submission_id": 1,
      "authentic_learning_score": 0.82,
      "intervention_needed": false,
      "created_at": "2024-12-01T10:30:00"
    }
  ]
}
```

### **❓ Quiz Endpoints**

#### **Get Quiz by ID**
```http
GET /api/quizzes/{quiz_id}
```

**Response:**
```json
{
  "id": 1,
  "student_id": 1,
  "submission_id": 1,
  "questions": [
    {
      "id": 1,
      "question": "What is the purpose of the calculate_fibonacci function?",
      "options": [
        "To calculate the nth Fibonacci number",
        "To calculate the sum of numbers",
        "To find the maximum number",
        "To sort numbers"
      ],
      "correct_answer": 0,
      "explanation": "The function uses recursion to calculate Fibonacci numbers"
    }
  ],
  "difficulty": "intermediate",
  "focus_areas": ["recursion", "algorithm design"],
  "created_at": "2024-12-01T10:30:00"
}
```

#### **Get All Quizzes**
```http
GET /api/quizzes
```

**Response:**
```json
{
  "quizzes": [
    {
      "id": 1,
      "student_id": 1,
      "submission_id": 1,
      "question_count": 5,
      "difficulty": "intermediate",
      "created_at": "2024-12-01T10:30:00"
    }
  ]
}
```

## 📊 **Data Models**

### **Student Model**
```json
{
  "id": 1,
  "student_id": "CS101015",
  "class_code": "CS101",
  "is_active": true,
  "created_at": "2024-12-01T10:30:00",
  "updated_at": "2024-12-01T10:30:00"
}
```

### **Submission Model**
```json
{
  "id": 1,
  "student_id": 1,
  "github_repo": "CS101/Python Calculator",
  "commit_sha": "direct-20241201103000",
  "commit_message": "Implemented basic calculator with GUI",
  "commit_date": "2024-12-01T10:30:00",
  "files_changed": ["calculator.py", "README.md"],
  "lines_added": 150,
  "lines_deleted": 0,
  "diff_content": "{\"calculator.py\": \"def calculate...\"}",
  "created_at": "2024-12-01T10:30:00"
}
```

### **Analysis Model**
```json
{
  "id": 1,
  "student_id": 1,
  "submission_id": 1,
  "historical_analysis": {
    "learning_trajectory": "gradual",
    "consistency_score": 0.85,
    "improvement_rate": 0.12,
    "pattern_anomalies": []
  },
  "tool_dependency": {
    "ai_usage_probability": 0.15,
    "copilot_usage_probability": 0.05,
    "copy_paste_probability": 0.02,
    "confidence": 0.78
  },
  "learning_progression": {
    "overall_progression": "positive",
    "skill_development_rate": 0.08,
    "understanding_level": "intermediate"
  },
  "authentic_learning_assessment": {
    "authentic_learning_score": 0.82,
    "genuine_understanding": true,
    "gradual_improvement": true,
    "consistent_approach": true
  },
  "intervention_recommendations": {
    "intervention_needed": false,
    "intervention_type": "none",
    "specific_recommendations": [],
    "priority": "low"
  },
  "created_at": "2024-12-01T10:30:00"
}
```

### **Quiz Model**
```json
{
  "id": 1,
  "student_id": 1,
  "submission_id": 1,
  "questions": [
    {
      "id": 1,
      "question": "What is the purpose of the calculate_fibonacci function?",
      "options": [
        "To calculate the nth Fibonacci number",
        "To calculate the sum of numbers",
        "To find the maximum number",
        "To sort numbers"
      ],
      "correct_answer": 0,
      "explanation": "The function uses recursion to calculate Fibonacci numbers"
    }
  ],
  "difficulty": "intermediate",
  "focus_areas": ["recursion", "algorithm design"],
  "created_at": "2024-12-01T10:30:00"
}
```

## 🚨 **Error Responses**

### **400 Bad Request**
```json
{
  "detail": "Validation error: [specific error message]"
}
```

### **404 Not Found**
```json
{
  "detail": "Resource not found"
}
```

### **500 Internal Server Error**
```json
{
  "detail": "Internal server error: [error message]"
}
```

## 📝 **Usage Examples**

### **Upload Code Submission (cURL)**
```bash
curl -X POST http://localhost:8000/api/upload/code \
  -F "student_id=CS101015" \
  -F "class_code=CS101" \
  -F "assignment_name=Python Calculator" \
  -F "commit_message=Implemented basic calculator with GUI" \
  -F "files=@calculator.py" \
  -F "files=@README.md"
```

### **Get Student Submissions (cURL)**
```bash
curl http://localhost:8000/api/upload/submissions/1
```

### **Get All Students (cURL)**
```bash
curl http://localhost:8000/api/upload/students
```

### **Upload Code Submission (Python)**
```python
import requests

files = [
    ('files', ('calculator.py', open('calculator.py', 'rb'))),
    ('files', ('README.md', open('README.md', 'rb')))
]

data = {
    'student_id': 'CS101015',
    'class_code': 'CS101',
    'assignment_name': 'Python Calculator',
    'commit_message': 'Implemented basic calculator with GUI'
}

response = requests.post(
    'http://localhost:8000/api/upload/code',
    files=files,
    data=data
)

print(response.json())
```

### **Upload Code Submission (JavaScript)**
```javascript
const formData = new FormData();
formData.append('student_id', 'CS101015');
formData.append('class_code', 'CS101');
formData.append('assignment_name', 'Python Calculator');
formData.append('commit_message', 'Implemented basic calculator with GUI');

// Add files
const fileInput = document.getElementById('files');
for (let file of fileInput.files) {
    formData.append('files', file);
}

fetch('http://localhost:8000/api/upload/code', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🔒 **Privacy Notes**

- **No personal information** is collected or stored
- **Student IDs** are anonymous identifiers
- **Class codes** are used for organization only
- **All data** is anonymized for analysis
- **FERPA/GDPR compliant** design

## 📞 **Support**

For API-related issues:
1. Check the `/docs` endpoint for interactive documentation
2. Review error messages in responses
3. Test with the provided examples
4. Check server logs for detailed error information

---

**🎉 API ready for privacy-focused educational use!** 
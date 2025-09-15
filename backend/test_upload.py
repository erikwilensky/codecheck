#!/usr/bin/env python3
"""
Test script for the direct upload system
"""

import requests
import os
import tempfile
import json

def create_test_file(content, filename):
    """Create a temporary test file"""
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return file_path

def test_upload():
    """Test the upload endpoint"""
    
    # Create test files
    python_code = '''
def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number"""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

def main():
    n = 10
    result = calculate_fibonacci(n)
    print(f"The {n}th Fibonacci number is {result}")

if __name__ == "__main__":
    main()
'''
    
    readme_content = '''
# Fibonacci Calculator

This program calculates Fibonacci numbers using recursion.

## Usage
Run the program and it will calculate the 10th Fibonacci number.

## Features
- Recursive implementation
- Clear documentation
- Error handling
'''
    
    # Create temporary files
    python_file = create_test_file(python_code, "fibonacci.py")
    readme_file = create_test_file(readme_content, "README.md")
    
    try:
        # Prepare the upload data
        files = [
            ('files', ('fibonacci.py', open(python_file, 'rb'), 'text/plain')),
            ('files', ('README.md', open(readme_file, 'rb'), 'text/plain'))
        ]
        
        data = {
            'student_id': 'STU001',
            'class_code': 'CS101',
            'assignment_name': 'Fibonacci Calculator',
            'commit_message': 'Implemented recursive Fibonacci calculator with documentation'
        }
        
        print("🚀 Testing upload endpoint...")
        print(f"📁 Files: {[f[1][0] for f in files]}")
        print(f"🆔 Student ID: {data['student_id']}")
        print(f"📚 Class Code: {data['class_code']}")
        print(f"📝 Assignment: {data['assignment_name']}")
        print(f"💬 Commit: {data['commit_message']}")
        print("-" * 50)
        
        # Make the request
        response = requests.post(
            'http://localhost:8000/api/upload/code',
            files=files,
            data=data
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Upload successful!")
            print(f"📋 Submission ID: {result['submission_id']}")
            print(f"🔍 Analysis ID: {result['analysis_id']}")
            print(f"❓ Quiz ID: {result['quiz_id']}")
            print(f"💬 Message: {result['message']}")
            
            # Test getting student submissions
            print("\n📚 Testing student submissions endpoint...")
            submissions_response = requests.get(
                f'http://localhost:8000/api/upload/submissions/{result.get("student_id", 1)}'
            )
            
            if submissions_response.status_code == 200:
                submissions = submissions_response.json()
                print(f"✅ Found {len(submissions['submissions'])} submissions for student")
                for sub in submissions['submissions']:
                    print(f"  - {sub['assignment']}: {sub['commit_message']}")
            else:
                print(f"❌ Failed to get submissions: {submissions_response.status_code}")
                
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        
    finally:
        # Clean up temporary files
        try:
            os.unlink(python_file)
            os.unlink(readme_file)
            os.rmdir(os.path.dirname(python_file))
        except:
            pass

def test_web_interface():
    """Test if the web interface is accessible"""
    try:
        print("\n🌐 Testing web interface...")
        response = requests.get('http://localhost:8000/upload')
        
        if response.status_code == 200:
            print("✅ Upload page is accessible!")
            print("🌍 You can now visit: http://localhost:8000/upload")
        else:
            print(f"❌ Upload page not accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error accessing web interface: {str(e)}")

if __name__ == "__main__":
    print("🧪 Testing Direct Upload System")
    print("=" * 50)
    
    # Test the upload endpoint
    test_upload()
    
    # Test the web interface
    test_web_interface()
    
    print("\n" + "=" * 50)
    print("🎉 Test completed!")
    print("\n📋 Next steps:")
    print("1. Visit http://localhost:8000/upload to use the web interface")
    print("2. Visit http://localhost:8000/docs to see the API documentation")
    print("3. Check the database for the test submission") 
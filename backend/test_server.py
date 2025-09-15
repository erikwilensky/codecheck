#!/usr/bin/env python3
"""
Test script to verify the server is working
"""

import requests
import time
import sys

def test_server():
    """Test if the server is running and responding"""
    
    print("🧪 Testing server...")
    print("=" * 30)
    
    # Wait a moment for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    # Test health endpoint
    try:
        response = requests.get("http://127.0.0.1:8002/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"📊 Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False
    
    # Test root endpoint
    try:
        response = requests.get("http://127.0.0.1:8002/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False
    
    # Test upload page
    try:
        response = requests.get("http://127.0.0.1:8002/upload", timeout=5)
        if response.status_code == 200:
            print("✅ Upload page working")
            if "Code Submission Portal" in response.text:
                print("✅ Upload page content correct")
            else:
                print("⚠️ Upload page content may be incorrect")
        else:
            print(f"❌ Upload page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Upload page error: {e}")
        return False
    
    # Test API docs
    try:
        response = requests.get("http://127.0.0.1:8002/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API docs working")
        else:
            print(f"❌ API docs failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API docs error: {e}")
        return False
    
    print("\n" + "=" * 30)
    print("🎉 All server tests passed!")
    print("\n📋 Access your system at:")
    print("🌐 Upload Page: http://127.0.0.1:8002/upload")
    print("📚 API Docs: http://127.0.0.1:8002/docs")
    print("📊 Health: http://127.0.0.1:8002/health")
    print("\n🚀 Your privacy-focused code assessment system is ready!")
    
    return True

if __name__ == "__main__":
    success = test_server()
    sys.exit(0 if success else 1) 
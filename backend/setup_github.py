#!/usr/bin/env python3
"""
GitHub Setup Script for AI Code Assessment System
Helps configure GitHub environment variables and test the setup
"""

import os
import sys
import requests
import json
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has GitHub variables"""
    env_file = Path(__file__).parent / '.env'
    
    if not env_file.exists():
        print("❌ .env file not found!")
        print("Please run: cp env.example .env")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    missing_vars = []
    required_vars = ['GITHUB_ACCESS_TOKEN', 'GITHUB_WEBHOOK_SECRET']
    
    for var in required_vars:
        if f"{var}=" not in content or f"{var}=your_" in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing GitHub variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ .env file found with GitHub variables")
    return True

def test_github_token():
    """Test GitHub access token"""
    token = os.getenv('GITHUB_ACCESS_TOKEN')
    
    if not token or token.startswith('your_'):
        print("❌ GitHub access token not configured")
        return False
    
    try:
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.get('https://api.github.com/user', headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ GitHub token valid - Authenticated as: {user_data.get('login', 'Unknown')}")
            return True
        else:
            print(f"❌ GitHub token invalid - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing GitHub token: {e}")
        return False

def test_webhook_endpoint():
    """Test webhook endpoint"""
    try:
        # Test basic webhook endpoint
        test_payload = {
            "ref": "refs/heads/main",
            "repository": {
                "name": "test-repo",
                "full_name": "test/test-repo"
            },
            "commits": [{
                "id": "abc123",
                "message": "Test commit",
                "author": {
                    "name": "Test Student",
                    "email": "student@example.com"
                },
                "added": [],
                "modified": ["main.py"],
                "removed": []
            }]
        }
        
        headers = {
            'Content-Type': 'application/json',
            'X-GitHub-Event': 'push'
        }
        
        response = requests.post(
            'http://localhost:8080/api/github/webhook',
            json=test_payload,
            headers=headers
        )
        
        if response.status_code in [200, 201]:
            print("✅ Webhook endpoint responding correctly")
            return True
        else:
            print(f"⚠️  Webhook endpoint status: {response.status_code}")
            print("Make sure the server is running on port 8080")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to webhook endpoint")
        print("Make sure the server is running: python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080")
        return False
    except Exception as e:
        print(f"❌ Error testing webhook: {e}")
        return False

def generate_webhook_secret():
    """Generate a secure webhook secret"""
    import secrets
    return secrets.token_urlsafe(32)

def setup_github_env():
    """Interactive setup for GitHub environment variables"""
    print("🔧 GitHub Environment Setup")
    print("=" * 40)
    
    # Check if .env exists
    env_file = Path(__file__).parent / '.env'
    if not env_file.exists():
        print("Creating .env file from template...")
        env_example = Path(__file__).parent / 'env.example'
        if env_example.exists():
            with open(env_example, 'r') as f:
                content = f.read()
            with open(env_file, 'w') as f:
                f.write(content)
    
    # Read current .env
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Update GitHub variables
    updated_lines = []
    github_token_set = False
    webhook_secret_set = False
    
    for line in lines:
        if line.startswith('GITHUB_ACCESS_TOKEN='):
            if 'your_github_token_here' in line:
                token = input("Enter your GitHub Personal Access Token: ").strip()
                if token:
                    updated_lines.append(f'GITHUB_ACCESS_TOKEN={token}\n')
                    github_token_set = True
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
                github_token_set = True
        elif line.startswith('GITHUB_WEBHOOK_SECRET='):
            if 'your_webhook_secret_here' in line:
                secret = input("Enter webhook secret (or press Enter to generate): ").strip()
                if not secret:
                    secret = generate_webhook_secret()
                    print(f"Generated webhook secret: {secret}")
                updated_lines.append(f'GITHUB_WEBHOOK_SECRET={secret}\n')
                webhook_secret_set = True
            else:
                updated_lines.append(line)
                webhook_secret_set = True
        else:
            updated_lines.append(line)
    
    # Write updated .env
    with open(env_file, 'w') as f:
        f.writelines(updated_lines)
    
    print("\n✅ Environment variables updated!")
    
    if github_token_set and webhook_secret_set:
        print("\n📋 Next Steps:")
        print("1. Test GitHub token: python setup_github.py --test-token")
        print("2. Start server: python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080")
        print("3. Test webhook: python setup_github.py --test-webhook")
        print("4. Set up GitHub webhooks using the webhook secret")

def main():
    """Main setup function"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--setup':
            setup_github_env()
            return
        elif sys.argv[1] == '--test-token':
            if test_github_token():
                print("✅ GitHub token is working correctly!")
            else:
                print("❌ GitHub token needs to be configured")
            return
        elif sys.argv[1] == '--test-webhook':
            if test_webhook_endpoint():
                print("✅ Webhook endpoint is working correctly!")
            else:
                print("❌ Webhook endpoint needs to be configured")
            return
        elif sys.argv[1] == '--check':
            print("🔍 GitHub Setup Check")
            print("=" * 30)
            
            env_ok = check_env_file()
            token_ok = test_github_token()
            webhook_ok = test_webhook_endpoint()
            
            print(f"\n📊 Summary:")
            print(f"   Environment File: {'✅' if env_ok else '❌'}")
            print(f"   GitHub Token: {'✅' if token_ok else '❌'}")
            print(f"   Webhook Endpoint: {'✅' if webhook_ok else '❌'}")
            
            if env_ok and token_ok and webhook_ok:
                print("\n🎉 GitHub setup is complete!")
            else:
                print("\n⚠️  Some issues need to be resolved")
            return
    
    # Default interactive setup
    print("🔗 GitHub Integration Setup")
    print("=" * 40)
    print("This script will help you configure GitHub integration.")
    print("\nOptions:")
    print("  --setup      Interactive setup for GitHub variables")
    print("  --test-token Test GitHub access token")
    print("  --test-webhook Test webhook endpoint")
    print("  --check      Check all GitHub configuration")
    print("\nExample:")
    print("  python setup_github.py --setup")

if __name__ == "__main__":
    main() 
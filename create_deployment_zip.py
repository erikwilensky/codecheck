#!/usr/bin/env python3
"""
Script to create a clean zip file for PythonAnywhere deployment
"""

import os
import zipfile
import shutil
from pathlib import Path

def create_deployment_zip():
    """Create a clean zip file for deployment"""
    
    # Files and directories to include
    include_patterns = [
        'app/',
        'static/',
        'requirements.txt',
        'wsgi.py',
        'pythonanywhere_setup.py',
        'PYTHONANYWHERE_DEPLOYMENT.md',
        'DEPLOYMENT_CHECKLIST.md',
        'UPLOAD_GUIDE.md',
        'env.example'
    ]
    
    # Files and directories to exclude
    exclude_patterns = [
        '__pycache__/',
        '.git/',
        '.vscode/',
        '*.pyc',
        '*.pyo',
        '*.log',
        '.DS_Store',
        'Thumbs.db',
        '*.zip'
    ]
    
    zip_name = 'code_share_deployment.zip'
    
    print(f"Creating deployment zip: {zip_name}")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for pattern in include_patterns:
            path = Path(pattern)
            if path.exists():
                if path.is_file():
                    print(f"Adding file: {pattern}")
                    zipf.write(pattern)
                elif path.is_dir():
                    print(f"Adding directory: {pattern}")
                    for root, dirs, files in os.walk(pattern):
                        # Skip excluded directories
                        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.vscode']]
                        
                        for file in files:
                            # Skip excluded files
                            if any(file.endswith(ext) for ext in ['.pyc', '.pyo', '.log', '.zip']):
                                continue
                            
                            file_path = os.path.join(root, file)
                            arc_path = file_path
                            print(f"  Adding: {file_path}")
                            zipf.write(file_path, arc_path)
    
    print(f"\n✅ Deployment zip created: {zip_name}")
    print(f"📁 Size: {os.path.getsize(zip_name) / 1024:.1f} KB")
    print("\n📋 Next steps:")
    print("1. Upload this zip file to PythonAnywhere")
    print("2. Extract it in your home directory")
    print("3. Follow the deployment guide")

if __name__ == "__main__":
    create_deployment_zip() 
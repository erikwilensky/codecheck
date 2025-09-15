import sys
import os

# Add your project directory to Python path
# Update this path to match your PythonAnywhere username and project location
path = '/home/yourusername/code_share'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
# These will be configured in PythonAnywhere's web app settings
os.environ['OPENAI_API_KEY'] = 'your_openai_api_key_here'
os.environ['DATABASE_URL'] = 'sqlite:///./ai_assessment.db'
os.environ['ADMIN_PASSWORD'] = 'your_secure_admin_password'

# Import your FastAPI app
from app.main import app

# For WSGI
application = app 
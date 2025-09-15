import sys
import os

# Add your project directory to Python path
# IMPORTANT: Replace 'yourusername' with your actual PythonAnywhere username
path = '/home/ewilensky/ai-assessment-system'
if path not in sys.path:
    sys.path.append(path)

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed, using environment variables only")

# Validate required environment variables
required_vars = ['OPENAI_API_KEY', 'ADMIN_PASSWORD']
missing_vars = []

for var in required_vars:
    if not os.getenv(var):
        missing_vars.append(var)

if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}. "
                    f"Please create a .env file or set these in PythonAnywhere environment.")

# Set default values for optional variables
if not os.getenv('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:///./ai_assessment.db'

# Import your FastAPI app
from app.main import app

# Create WSGI-compatible application for PythonAnywhere
def application(environ, start_response):
    """WSGI application entry point for PythonAnywhere"""
    return app(environ, start_response) 
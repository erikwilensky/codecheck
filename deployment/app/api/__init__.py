from .github_webhook import router as github_router
from .students import router as students_router
from .submissions import router as submissions_router
from .analyses import router as analyses_router
from .quizzes import router as quizzes_router
from .upload import router as upload_router
from .admin import router as admin_router

__all__ = ['github_router', 'students_router', 'submissions_router', 'analyses_router', 'quizzes_router', 'upload_router', 'admin_router'] 
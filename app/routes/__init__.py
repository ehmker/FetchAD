from .home import router as home_router
from .dashboard import router as dashboard_router
from .reports import router as reports_router
from .login import router as login_router
from .actions import router as actions_router
from .users import router as users_router

routers = [
    home_router,
    dashboard_router,
    reports_router,
    login_router,
    actions_router,
    users_router,
]

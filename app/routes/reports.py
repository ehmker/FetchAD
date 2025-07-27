from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.auth import require_auth, extract_credentials
from app.services.ad_actions import get_locked_users, get_expired_users


templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/report/locked_users", response_class=HTMLResponse)
def locked_users(request: Request, session=Depends(require_auth)):
    locked_users_data = get_locked_users(*extract_credentials(session))

    return templates.TemplateResponse(
        "locked_users.html",
        {
            "request": request,
            "user": session["username"],
            "locked_users": locked_users_data,
        },
    )


@router.get("/report/expired_password_users", response_class=HTMLResponse)
def expired_users(request: Request, session=Depends(require_auth)):
    expired_users_data = get_expired_users(*extract_credentials(session))

    return templates.TemplateResponse(
        "expired_users.html",
        {
            "request": request,
            "user": session["username"],
            "expired_users": expired_users_data,
        },
    )

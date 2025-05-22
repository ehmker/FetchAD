from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.auth import get_current_user
from app.services.ad_actions import get_locked_users, get_expired_users


templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/report/locked_users", response_class=HTMLResponse)
def locked_users(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)
    # Mocked data - replace later with real LDAP or AD queries
    # locked_users_data = [
    #     {
    #         "username": "jdoe",
    #         "name": "John Doe",
    #         "email": "jdoe@email.com",
    #         "status": "Locked Out",
    #     },
    #     {
    #         "username": "asmith",
    #         "name": "Alice Smith",
    #         "email": "asmith@email.com",
    #         "status": "Locked Out",
    #     },
    # ]
    locked_users_data = get_locked_users()

    return templates.TemplateResponse(
        "locked_users.html",
        {"request": request, "user": user, "locked_users": locked_users_data},
    )


@router.get("/report/expired_password_users", response_class=HTMLResponse)
def expired_users(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)
    
    expired_users_data = get_expired_users()

    return templates.TemplateResponse(
        'expired_users.html',
        {"request": request, "user": user, "expired_users": expired_users_data}
    )
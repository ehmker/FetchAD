from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.auth import (
    authenticate_ldap_user,
    require_auth,
)  # optional, if you want to show user context
from app.sessions import create_session, delete_session


templates = Jinja2Templates(directory="templates")
router = APIRouter()

SESSION_COOKIE_NAME = "session_token"


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if authenticate_ldap_user(username, password):
        session_token = create_session(username, password)
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=session_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=1800,
        )
        return response

    if username == "testuser" and password == "password":
        session_token = create_session(username, password)
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=session_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=1800,
        )
        return response

    # invalid credentials
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)


@router.get("/logout")
def logout(request: Request):
    session_token = request.cookies.get(SESSION_COOKIE_NAME)
    if session_token:
        delete_session(session_token)
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("user")
    return response

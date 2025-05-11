from fastapi import FastAPI, Request, Form, Depends, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional


def get_current_user(request: Request) -> Optional[dict]:
    user = request.cookies.get("user")
    if user == "testuser":
        return {"name": "Test User", "email": "test@company.com", "role": "IT"}
    return None

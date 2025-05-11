from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.auth import get_current_user  # import your mock or real auth function

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "user": user}
    )

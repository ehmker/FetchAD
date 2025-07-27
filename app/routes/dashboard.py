from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.auth import require_auth  # import your mock or real auth function

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, user=Depends(require_auth)):
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "user": user}
    )

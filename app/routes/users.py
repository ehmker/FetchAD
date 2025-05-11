from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette import status

# from app.services.ad_actions import create_user  # your backend logic

templates = Jinja2Templates(directory="templates")
router = APIRouter()
DEPARTMENT_JOBS = {
    "IT": ["Helpdesk Technician", "System Administrator", "Network Engineer"],
    "HR": ["HR Coordinator", "Recruiter", "Benefits Specialist"],
    "Finance": ["Accountant", "Controller", "Financial Analyst"],
}


@router.get("/users/create", response_class=HTMLResponse)
def show_create_user_form(request: Request):
    departments = list(DEPARTMENT_JOBS.keys())
    return templates.TemplateResponse(
        "create_user.html",
        {"request": request, "departments": departments, "job_titles": DEPARTMENT_JOBS},
    )


@router.post("/users/create")
def handle_create_user(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    department: str = Form(None),
):
    success = create_user(
        first_name=first_name,
        last_name=last_name,
        username=username,
        password=password,
        department=department,
    )

    if success:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return templates.TemplateResponse(
            "create_user.html", {"request": request, "error": "Failed to create user"}
        )

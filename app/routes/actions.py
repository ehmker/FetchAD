from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from starlette import status
from app.services import ad_actions

router = APIRouter()


@router.post("/actions/unlock_user")
def unlock_user(user_dn: str = Form(...)):
    print(f"Received unlock request for: {user_dn}")
    ad_actions.unlock_user(user_dn)
    return RedirectResponse(
        url="/report/locked_users", status_code=status.HTTP_303_SEE_OTHER
    )

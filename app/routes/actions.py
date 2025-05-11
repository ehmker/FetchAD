from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from starlette import status

router = APIRouter()


@router.post("/actions/unlock_user")
def unlock_user(username: str = Form(...)):
    # 🔓 Replace this with actual logic to unlock the AD user
    print(f"Received unlock request for: {username}")

    # Temporary success message (or redirect to dashboard)
    return RedirectResponse(
        url="/report/locked_users", status_code=status.HTTP_303_SEE_OTHER
    )

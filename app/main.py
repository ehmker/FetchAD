from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.exception_handlers import http_exception_handler
from app.routes import routers
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()
for router in routers:
    app.include_router(router)


@app.exception_handler(StarletteHTTPException)
async def redirect_on_unauth(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 401:
        return RedirectResponse(url="/login")
    return await http_exception_handler(request, exc)

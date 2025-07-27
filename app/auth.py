from fastapi import Request, HTTPException
from typing import Optional
from app.services.ad_connection import ldap_connection
from app.sessions import get_session, decrypt_password

SESSION_COOKIE_NAME = "session_token"


def authenticate_ldap_user(username: str, password: str) -> bool:
    try:
        with ldap_connection(username, password) as conn:
            return conn.bind
    except Exception as e:
        print("LDAP authentication error: ", e)
        return False


def require_auth(request: Request):
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Authentication required")

    session = get_session(token)
    if not session:
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    return session


def extract_credentials(session):
    return session["username"], decrypt_password(session["password"])

import redis
import json
import os
from cryptography.fernet import Fernet
from uuid import uuid4

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
FERNET_KEY = os.getenv("FERNET_KEY", Fernet.generate_key())
SESSION_EXPIRE_SECONDS = 1800  # 30 Min

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
fernet = Fernet(FERNET_KEY)


def create_session(username: str, password: str) -> str:
    session_token = str(uuid4())
    session_data = {
        "username": username,
        "password": encrypt_password(password),
    }
    r.setex(session_token, SESSION_EXPIRE_SECONDS, json.dumps(session_data))
    return session_token


def get_session(session_token: str):
    data = r.get(session_token)
    if not data:
        return None
    return json.loads(data)


def delete_session(session_token: str):
    r.delete(session_token)


def encrypt_password(password_plain_text: str):
    return fernet.encrypt(password_plain_text.encode()).decode()


def decrypt_password(password_encrypted):
    return fernet.decrypt(password_encrypted.encode()).decode()

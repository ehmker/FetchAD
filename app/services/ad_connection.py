from ldap3 import Server, Connection, ALL
from contextlib import contextmanager
import os


def ldap_connection():
    conn = get_ldap_connection()
    try:
        yield conn
    finally:
        conn.unbind()


def get_ldap_connection() -> Connection:
    # Replace with actual connection
    server = Server()
    conn = Connection()

    return conn


# app/services/ad_service.py
def get_all_users():
    # Placeholder — later this will run ldap3 queries
    return [{"username": "jsmith"}, {"username": "adoe"}]

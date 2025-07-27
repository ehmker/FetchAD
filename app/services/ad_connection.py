from ldap3 import Server, Connection, ALL, NTLM
from contextlib import contextmanager
from dotenv import load_dotenv
import os

load_dotenv()
DOMAIN = os.getenv("DOMAIN")
AD_SERVER = os.getenv("AD_SERVER")


@contextmanager
def ldap_connection(username: str, password: str):
    conn = get_ldap_connection(username, password)
    try:
        yield conn
    finally:
        conn.unbind()


def get_ldap_connection(username: str, password: str) -> Connection:
    # Function returns a connection object to perform ldap actions with
    try:
        server = Server(AD_SERVER, get_info=ALL)
        conn = Connection(
            server,
            user=f"{DOMAIN}\\{username}",
            password=password,
            authentication="NTLM",
        )

        return conn
    except Exception as e:
        print("an error occured getting ldap connection:", e)
        raise


# app/services/ad_service.py
def get_all_users():
    # Placeholder — later this will run ldap3 queries
    return [{"username": "jsmith"}, {"username": "adoe"}]

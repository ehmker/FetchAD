from ldap3 import Server, Connection, ALL, NTLM
from contextlib import contextmanager
from dotenv import load_dotenv
import os

load_dotenv()
AD_SERVER = os.getenv('AD_SERVER')
AD_USER = os.getenv('USER_NAME')
AD_PASSWORD = os.getenv('PW')

@contextmanager
def ldap_connection():
    conn = get_ldap_connection()
    try:
        yield conn
    finally:
        conn.unbind()


def get_ldap_connection() -> Connection:
    # Function returns a connection object to perform ldap actions with
    try: 
        server = Server(AD_SERVER, get_info=ALL)
        conn = Connection(server, user=AD_USER, password=AD_PASSWORD, authentication='NTLM')
    except Exception as e:
        print('an error occured getting ldap connection:', e)
    return conn


# app/services/ad_service.py
def get_all_users():
    # Placeholder — later this will run ldap3 queries
    return [{"username": "jsmith"}, {"username": "adoe"}]

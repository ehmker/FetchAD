from app.services.ad_connection import ldap_connection
from ldap3 import MODIFY_REPLACE


def unlock_user(username: str) -> bool:
    with ldap_connection as conn:

        user_dn = f"CN={username},OU=Users,DC=your,DC=domain"

        success = conn.modify(user_dn, {"lockoutTime": [(MODIFY_REPLACE, ["0"])]})

    return success

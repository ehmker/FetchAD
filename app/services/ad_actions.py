from app.services.ad_connection import ldap_connection
from ldap3 import MODIFY_REPLACE, SUBTREE
from datetime import datetime, timedelta, timezone


BASE_DN = 'DC=CO,DC=ITASCA'

def date_time_to_windows_filetime(dt: datetime) -> int:
    WINDOWS_EPOCH = datetime(1601, 1, 1, tzinfo=timezone.utc)
    return int((dt - WINDOWS_EPOCH).total_seconds() * 10**7)

def unlock_user(user_dn: str) -> bool:
    with ldap_connection as conn:
        success = conn.modify(user_dn, {"lockoutTime": [(MODIFY_REPLACE, ["0"])]})

    return success

def get_locked_users():
    two_hours_ago = datetime.now(timezone.utc) - timedelta(hours=2)
    filetime_cutoff = date_time_to_windows_filetime(two_hours_ago)

    SEARCH_FILTER = f'''
            (&
                (lockoutTime>={filetime_cutoff})
                (objectclass=person) 
                (!(userAccountControl:1.2.840.113556.1.4.803:=2))
            )
            '''

    with ldap_connection() as conn:
        if conn.bind():
            conn.search(
                search_base=BASE_DN,
                search_filter=SEARCH_FILTER,
                search_scope=SUBTREE,
                attributes=['sAMAccountName','displayName', 'mail', 'distinguishedName']
            )
            if conn.entries:
                for entry in conn.entries:
                    entry.entry_to_json()

            return conn.entries
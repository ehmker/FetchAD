from app.services.ad_connection import ldap_connection
from ldap3 import MODIFY_REPLACE, SUBTREE
from datetime import datetime, timedelta, timezone
import json

BASE_DN = 'DC=CO,DC=ITASCA'
ITASCA_USERS_DN = 'OU=Itasca Users,DC=CO,DC=ITASCA'




def datetime_to_filetime(dt: datetime) -> int:
    return int((dt- datetime(1601, 1, 1, tzinfo=timezone.utc)).total_seconds() * 10**7)

def filetime_to_datetime(ft: int) -> datetime:
    return datetime(1601, 1, 1, tzinfo=timezone.utc) + timedelta(microseconds=int(ft) / 10)

def get_days_to_expiration(pwd_last_set, pwd_lifetime=60):
    expiration = pwd_last_set + timedelta(days=pwd_lifetime)
    days_remaining = (expiration - datetime.now(timezone.utc)).days + 1
    return expiration, days_remaining

def expiration_status_from_days_left(days: int) -> str:
    if days is None:
        return 'Unknown'
    if days < 0: 
        return 'Expired'
    elif days < 15: 
        return 'Expiring Soon'
    else:
        return 'Valid'

def entry_to_dict(e) -> dict:
    raw_json = e.entry_to_json()
    parsed = json.loads(raw_json)
    return parsed['attributes']

def unlock_user(user_dn: str) -> bool:
    with ldap_connection() as conn:
        if conn.bind():
            success = conn.modify(user_dn, {"lockoutTime": [(MODIFY_REPLACE, ["0"])]})

    return success

def get_locked_users():
    two_hours_ago = datetime.now(timezone.utc) - timedelta(hours=2)
    filetime_cutoff = datetime_to_filetime(two_hours_ago)
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
                search_base=ITASCA_USERS_DN,
                search_filter=SEARCH_FILTER,
                search_scope=SUBTREE,
                attributes=['sAMAccountName','displayName', 'mail', 'distinguishedName']
            )
            if conn.entries:
                return conn.entries
            else:
                return []

def get_expired_users():
    days_to_expiration = 7
    pwd_lifetime_days = 60
    cutoff = datetime.now(timezone.utc) - timedelta(days=(pwd_lifetime_days - days_to_expiration))
    filetime_cutoff = datetime_to_filetime(cutoff)
    SEARCH_FILTER = f'''
                    (&
                        (objectclass=person)
                        (pwdLastSet<={filetime_cutoff})
                        (!(userAccountControl:1.2.840.113556.1.4.803:=2))
                        (!(UserAccountControl:1.2.840.113556.1.4.803:=65536))
                        (logonCount>=1)
                    )
                    '''
                    # (!(userAccountControl:1.2.840.113556.1.4.803:=2)) --> Not flagged as disabled account
                    # (!(UserAccountControl:1.2.840.113556.1.4.803:=65536)) --> Not flagged with 'Password never expires'

    with ldap_connection() as conn:
        if conn.bind():
            conn.search(
                search_base=ITASCA_USERS_DN,
                search_filter=SEARCH_FILTER,
                search_scope=SUBTREE,
                attributes=['sAMAccountName','displayName', 'mail', 'pwdLastSet', 'department']
            )
        if conn.entries:
            conn.entries.sort(key=lambda e: e['pwdLastSet'].value, reverse=True)
            entries_as_dict = []
            for entry in conn.entries:
                entry_as_dict = entry_to_dict(entry)
                expires_on, days_left = get_days_to_expiration(entry.pwdLastSet.value)
                entry_as_dict['expire_on'] = expires_on
                entry_as_dict['days_left'] = days_left
                entry_as_dict['status'] = expiration_status_from_days_left(days_left) 
                entries_as_dict.append(entry_as_dict)

            return entries_as_dict
        
    return []
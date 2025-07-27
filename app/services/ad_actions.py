from app.services.ad_connection import ldap_connection
from ldap3 import MODIFY_REPLACE, SUBTREE
from datetime import datetime, timedelta, timezone
from app.tests import test_users_data
from app.utils.time import datetime_to_filetime, filetime_to_datetime
import json

BASE_DN = "DC=CO,DC=ITASCA"
ITASCA_USERS_DN = "OU=Itasca Users,DC=CO,DC=ITASCA"


def get_days_to_expiration(pwd_last_set, pwd_lifetime=60):
    if isinstance(pwd_last_set, int):
        pwd_last_set = filetime_to_datetime(pwd_last_set)

    expiration = pwd_last_set + timedelta(days=pwd_lifetime)
    days_remaining = (expiration - datetime.now(timezone.utc)).days + 1
    return expiration, days_remaining


def expiration_status_from_days_left(days: int) -> str:
    if days is None:
        return "Unknown"
    if days < 0:
        return "Expired"
    elif days < 15:
        return "Expiring Soon"
    else:
        return "Valid"


def entry_to_dict(e) -> dict:
    if hasattr(e, "entry_attributes"):
        raw_json = e.entry_to_json()
        parsed = json.loads(raw_json)
        return parsed["attributes"]
    else:
        entry_dict = {}
        for attr in dir(e):
            if attr.startswith("_"):
                continue
            value = getattr(e, attr)
            if callable(value):
                continue
            entry_dict[attr] = value
        return entry_dict


def unlock_user(user_dn: str) -> bool:
    with ldap_connection() as conn:
        if conn.bind():
            success = conn.modify(user_dn, {"lockoutTime": [(MODIFY_REPLACE, ["0"])]})

    return success


def get_locked_users(username, password):
    if username == "testuser":
        return test_users_data()
    two_hours_ago = datetime.now(timezone.utc) - timedelta(hours=2)
    filetime_cutoff = datetime_to_filetime(two_hours_ago)
    SEARCH_FILTER = f"""
            (&
                (lockoutTime>={filetime_cutoff})
                (objectclass=person) 
                (!(userAccountControl:1.2.840.113556.1.4.803:=2))
            )
            """

    with ldap_connection(username, password) as conn:
        if conn.bind():
            conn.search(
                search_base=ITASCA_USERS_DN,
                search_filter=SEARCH_FILTER,
                search_scope=SUBTREE,
                attributes=[
                    "sAMAccountName",
                    "displayName",
                    "mail",
                    "distinguishedName",
                ],
            )
            if conn.entries:
                return conn.entries
            else:
                return []


def get_expired_users(username, password):
    if username == "testuser":
        return _expired_users_format(test_users_data(), fake=True)
    days_to_expiration = 7
    pwd_lifetime_days = 60
    cutoff = datetime.now(timezone.utc) - timedelta(
        days=(pwd_lifetime_days - days_to_expiration)
    )
    filetime_cutoff = datetime_to_filetime(cutoff)
    SEARCH_FILTER = f"""
                    (&
                        (objectclass=person)
                        (pwdLastSet<={filetime_cutoff})
                        (!(userAccountControl:1.2.840.113556.1.4.803:=2))
                        (!(UserAccountControl:1.2.840.113556.1.4.803:=65536))
                        (logonCount>=1)
                    )
                    """
    # (!(userAccountControl:1.2.840.113556.1.4.803:=2)) --> Not flagged as disabled account
    # (!(UserAccountControl:1.2.840.113556.1.4.803:=65536)) --> Not flagged with 'Password never expires'

    with ldap_connection() as conn:
        if conn.bind():
            conn.search(
                search_base=ITASCA_USERS_DN,
                search_filter=SEARCH_FILTER,
                search_scope=SUBTREE,
                attributes=[
                    "sAMAccountName",
                    "displayName",
                    "mail",
                    "pwdLastSet",
                    "department",
                ],
            )
        if conn.entries:
            return _expired_users_format(conn.entries)

    return []


def _expired_users_format(entries, fake=False):
    def get_pwd_last_set(entry):
        try:
            return entry["pwdLastSet"].value
        except (TypeError, AttributeError, KeyError):
            return entry.pwdLastSet

    # Sort entries by pwdLastSet descending
    entries.sort(key=lambda e: get_pwd_last_set(e), reverse=True)

    entries_as_dict = []
    for entry in entries:
        entry_as_dict = entry_to_dict(entry)
        expires_on, days_left = get_days_to_expiration(entry_as_dict["pwdLastSet"])
        entry_as_dict["expire_on"] = expires_on
        entry_as_dict["days_left"] = days_left
        entry_as_dict["status"] = expiration_status_from_days_left(days_left)
        entries_as_dict.append(entry_as_dict)

    return entries_as_dict

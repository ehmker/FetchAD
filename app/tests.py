from datetime import datetime, timezone, timedelta
from faker import Faker
import random
from app.utils.time import datetime_to_filetime

fake = Faker()


class FakeLDAPEntry:
    def __init__(self, **attrs):
        self.__dict__.update(attrs)

    def __repr__(self):
        return f"<FakeLDAPEntry {self.sAMAccountName}>"


def generate_lastPwdSet():
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=67)
    end = now - timedelta(days=53)
    random_dt = fake.date_time_between(start_date=start, end_date=end)
    print(random_dt)
    return datetime_to_filetime(random_dt)


def generate_fake_ldap_user():
    # generate name
    first = fake.first_name()
    last = fake.last_name()
    return FakeLDAPEntry(
        sAMAccountName=f"{first[0]}{last}",
        displayName=f"{first} {last}",
        mail=f"{first}.{last}@testdomain.com",
        distinguishedName=f"CN={first} {last},OU=Users,DC=testdomain,DC=com",
        pwdLastSet=generate_lastPwdSet(),
        department=str().join(fake.random_letters(3)).upper(),
    )


def test_users_data():
    users = []

    for _ in range(random.randint(2, 10)):
        users.append(generate_fake_ldap_user())

    return users


# def test_

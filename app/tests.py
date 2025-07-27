from datetime import datetime, timezone, timedelta


class FakeLDAPEntry:
    def __init__(self, **attrs):
        self.__dict__.update(attrs)

    def __repr__(self):
        return f"<FakeLDAPEntry {self.sAMAccountName}>"


def test_locked_users_data():
    return [
        FakeLDAPEntry(
            sAMAccountName="jdoe",
            displayName="John Doe",
            mail="jdoe@example.com",
            distinguishedName="CN=John Doe,OU=Users,DC=example,DC=com",
        ),
        FakeLDAPEntry(
            sAMAccountName="asmith",
            displayName="Alice Smith",
            mail="asmith@example.com",
            distinguishedName="CN=Alice Smith,OU=Users,DC=example,DC=com",
        ),
    ]

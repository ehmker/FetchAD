from datetime import datetime, timedelta, timezone


def datetime_to_filetime(dt: datetime) -> int:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    base_date = datetime(1601, 1, 1, tzinfo=timezone.utc)
    return int((dt - base_date).total_seconds() * 10**7)


def filetime_to_datetime(ft: int) -> datetime:
    return datetime(1601, 1, 1, tzinfo=timezone.utc) + timedelta(
        microseconds=int(ft) / 10
    )

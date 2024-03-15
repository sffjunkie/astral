import datetime


def datetime_almost_equal(
    datetime1: datetime.datetime, datetime2: datetime.datetime, seconds: int = 60
):
    if datetime1.tzinfo:
        datetime1 = datetime1.astimezone(datetime.timezone.utc)
    else:
        datetime1 = datetime1.replace(tzinfo=datetime.timezone.utc)

    if datetime2.tzinfo:
        datetime2 = datetime2.astimezone(datetime.timezone.utc)
    else:
        datetime2 = datetime2.replace(tzinfo=datetime.timezone.utc)

    return abs((datetime1 - datetime2).total_seconds()) <= seconds

import datetime


def datetime_almost_equal(
    datetime1: datetime.datetime, datetime2: datetime.datetime, seconds: int = 60
):
    if not (datetime1.tzinfo):
        datetime1 = datetime1.replace(tzinfo=datetime.timezone.utc)
    else:
        datetime1 = datetime1.astimezone(datetime.timezone.utc)

    if not (datetime2.tzinfo):
        datetime2 = datetime2.replace(tzinfo=datetime.timezone.utc)
    else:
        datetime2 = datetime2.astimezone(datetime.timezone.utc)

    dd = datetime1 - datetime2
    sd = (dd.days * 24 * 60 * 60) + dd.seconds
    return abs(sd) <= seconds

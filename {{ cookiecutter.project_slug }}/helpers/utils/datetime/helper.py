import datetime
import zoneinfo

TAIWAN_TIMEZONE = zoneinfo.ZoneInfo("{{ cookiecutter.timezone }}")


def datetime_now() -> datetime.datetime:
    return datetime.datetime.now(tz=TAIWAN_TIMEZONE)

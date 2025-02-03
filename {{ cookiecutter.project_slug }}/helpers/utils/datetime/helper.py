import datetime
import zoneinfo

THIS_TIMEZONE = zoneinfo.ZoneInfo("{{ cookiecutter.timezone }}")


def datetime_now() -> datetime.datetime:
    return datetime.datetime.now(tz=THIS_TIMEZONE)

import datetime

from pydantic import BaseModel


class GetStatusResponse(BaseModel):
    runserver_datetime: datetime.datetime

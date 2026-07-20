from pydantic import BaseModel


class ApodResponse(BaseModel):
    date: str
    title: str
    explanation: str
    url: str
    media_type: str
    service_version: str
    hdurl: str | None = None
    copyright: str | None = None

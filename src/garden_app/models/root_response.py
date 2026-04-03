from typing import Literal

from pydantic import BaseModel, Field


class RootResponse(BaseModel):
    name: str = Field(examples=["Garden Tasks API"])
    version: str = Field(examples=["0.1.0"])
    status: Literal["ok"]

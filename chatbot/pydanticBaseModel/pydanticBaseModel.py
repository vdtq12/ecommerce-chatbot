from pydantic import BaseModel, Field
from typing import List, Optional

class appSystemReqs(BaseModel):
    """System requirements of an software"""

    name: str = Field(description="sofware name")
    softwareVersion: str = Field(description="software version")
    operatingSystem: List[str] = Field(description="list of operating system available")
    processor: List[str] = Field(description="list of processor available")
    memory: List[int] = Field(description="list of memory capacities, unit is GB")
    screenDisplay: str = Field(description="screen display information")
    displayCard: str = Field(description="display card information")


class Info(BaseModel):
    """Information to extract"""

    reqs: List[appSystemReqs]


class CustomerInput(BaseModel):
    """The question or the query of the customer"""

    query: str = Field(
        description="the question or the query of the customer, must include as much information as possible"
    )


class Software(BaseModel):
    """The name of the software that customer mentioned"""

    name: str = Field(description="software name")
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class appSystemReqs(BaseModel):
    """System requirements of an software"""

    name: str = Field(description="sofware name")
    operatingSystem: str = Field(description="operating system available")
    processor: str = Field(description="processor available")
    memory: str = Field(description="memory capacities, unit is GB")
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


class SoftwareHardwareRecommendations(BaseModel):
    """Include both the question or the query of the customer and name of the software that customer mentioned"""
    
    # query: str = Field(
    #     description="the question or the query of the customer, must include as much information as possible"
    # )
    # name: str = Field(description="software name")
    # sys_reqs: Info
    query: str = Field(
        description="""a string under dictionary format containing the following keys:

                            query: a string represent the question or the query of the customer, must include as much information as possible
                            softName: a strin represent, the software name
                            
                            example:
                            " "query": "a phone play LOL", "softName": "LOL"}" """
    )

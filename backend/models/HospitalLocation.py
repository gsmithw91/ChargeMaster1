from pydantic import BaseModel, ValidationError
from typing import Optional

class HospitalLocation(BaseModel):
    LocationID : Optional [int]
    SystemID : Optional [int]
    LocationName : Optional [str]
    Address : Optional [str]
    City : Optional [str]
    State : Optional [str]
    ZipCode : Optional [int]
    Phone : Optional [int]



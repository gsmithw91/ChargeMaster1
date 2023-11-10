from pydantic import BaseModel, ValidationError
from typing import Optional

class HospitalSystem(BaseModel):
    SystemID : Optional [int]
    SystemName : Optional [str]
    Headquarters : Optional [str]
    FoundedYear : Optional [int]
    Description : Optional [str]
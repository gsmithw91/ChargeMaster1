from pydantic import BaseModel, ValidationError
from typing import Optional

class HospitalSystem(BaseModel):
    SystemID : Optional [int] = None
    SystemName : Optional [str] = None
    Headquarters : Optional [str] = None
    FoundedYear : Optional [int] = None
    Description : Optional [str] = None
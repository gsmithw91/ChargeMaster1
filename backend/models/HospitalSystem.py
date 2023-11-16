from pydantic import BaseModel, ValidationError, validator
from typing import Optional

class HospitalSystem(BaseModel):
    SystemID : Optional [int] = None
    SystemName : Optional [str] = None
    Headquarters : Optional [str] = None
    FoundedYear : Optional [int] = None
    Description : Optional [str] = None
    
   
    @validator('FoundedYear', pre=True, allow_reuse=True)
    def parse_founded_year(cls, v):
        if v in ['NULL', 'null', 'Null', ''] or v is None:
            return None
        try:
            return int(v)
        except ValueError:
            raise ValueError(f"Invalid value for FoundedYear: {v}")
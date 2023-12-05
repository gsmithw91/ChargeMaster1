from pydantic import BaseModel, ValidationError
from typing import Optional

class Insurance_Type(BaseModel):
    InsuranceTypeID: Optional[int]
    InsuranceType: Optional[str]
    
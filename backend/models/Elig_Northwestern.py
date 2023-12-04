from pydantic import BaseModel
from typing import Optional

class Eligible_Insurance(BaseModel):
    EligibilityID: Optional[int]
    SystemID: Optional[int]
    LocationID: Optional[int]
    InsuranceTypeID: Optional[int]
    Carrier: Optional[str]
    InNetwork: Optional[bool]
    EligibilityYear: Optional[int]
    PlanName: Optional[str]

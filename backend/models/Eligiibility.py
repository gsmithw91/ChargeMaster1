from pydantic import BaseModel
from typing import Optional

class Eligible_Insurance(BaseModel):
    EligibilityID : Optional[int]
    SystemID : Optional[int]
    LocationID : Optional[int]
    InsuranceTypeID : Optional[int]
    CarrierName : Optional[str]
    CarrierID : Optional[int]   
    InNetwork : Optional[int]
    PlanName : Optional[str]
    PlanID : Optional[int]
    

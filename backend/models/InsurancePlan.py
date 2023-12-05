from pydantic import BaseModel, ValidationError
from typing import Optional

class Insurance_Plan(BaseModel):
      PlanID : Optional [int]
      CarrierID : Optional [int]
      InsuranceType : Optional [str]
      PlanName : Optional [str]
      InsuranceTypeID : Optional [int]
      
      
      
      
      
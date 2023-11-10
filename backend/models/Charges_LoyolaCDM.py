from pydantic import BaseModel, ValidationError
from typing import Optional


class LoyolaCDMCharges(BaseModel):
    LocationID : Optional [int]
    SystemID : Optional [int]
    CDMCode : Optional [str]
    ServiceDescription : Optional [float]
    DiscountedCashPrice : Optional [float]
    BillingCode : Optional [str]
    LocationName : Optional [str]
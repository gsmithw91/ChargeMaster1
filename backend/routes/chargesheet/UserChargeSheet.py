from pydantic import BaseModel
from typing import Optional

class UserChargeSheet(BaseModel):
    UserChargeSheetID: Optional[int]
    UserID: Optional[int]
    LocationID: Optional[int]
    SystemID: Optional[int]
    ChargeID: Optional[int]

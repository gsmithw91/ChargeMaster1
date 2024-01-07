from pydantic import BaseModel, ValidationError
from typing import Optional


class AgentModel(BaseModel):
    AgentID: int
    RecordID: Optional[int] = None
    AgentType: Optional[str] = None
    OrganizationName: Optional[str] = None
    PhoneNumber: Optional[str] = None
    Address: Optional[str] = None
    City: Optional[str] = None
    State: Optional[str] = None
    Zip: Optional[str] = None
    Languages_Offered: Optional[str] = None
    Org2nd: Optional[str] = None
    Office: Optional[str] = None
    TollFreePhone: Optional[str] = None

from pydantic import BaseModel, ValidationError
from typing import Optional



class AdvocateCharges(BaseModel):
    LocationID : Optional[int]
    SystemID : Optional[int]
    LocationName : Optional[str ]
    BillingCode : Optional[str]
    ServiceDescription : Optional[str]
    RevenueCode : Optional[str]
    GrossCharge : Optional[float]
    DeidentifiedMinimumCharge : Optional[float]
    DeidentifiedMaximumCharge : Optional[float]
    DiscountedCashPrice : Optional[float]
    AETNA509 : Optional [float]
    AETNAAPCNSP729 : Optional [float]
    AETNABP760 : Optional [float]
    AETNAILPREFERRED139 : Optional [float]
    BCBSBLUECHOICEOPTIONS727 : Optional [float]
    BCBSBLUECHOICEPREFERRED479 : Optional [float]
    BCBSPARINDEMNITYADP505 : Optional [float]
    BCBSPPO424 : Optional [float]
    CIGNAALTERNATIVE668 : Optional [float]
    CIGNABROAD667 : Optional [float]
    CIGNAPLUSNM682 : Optional [float]
    HUMANAHMO299 : Optional [float]
    HUMANAPPO145 : Optional [float]
    UHCCORE346 : Optional [float]
    UHCHMOPPO535 : Optional [float]
    ChargeCode : Optional [float]
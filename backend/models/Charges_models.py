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
    
    
class LoyolaCDMCharges(BaseModel):
    LocationID : Optional [int]
    SystemID : Optional [int]
    CDMCode : Optional [str]
    ServiceDescription : Optional [float]
    DiscountedCashPrice : Optional [float]
    BillingCode : Optional [str]
    LocationName : Optional [str]



class LoyolaCharges(BaseModel):
    LocationID : Optional [int]
    SystemID : Optional [int ]
    LocationName : Optional [str]
    BillingCode : Optional [str]
    ServiceDescription : Optional [str]
    GrossCharge : Optional [float]
    DeidentifiedMaximumCharge : Optional [float]
    DeidentifiedMinimumCharge : Optional [float]
    DerivedContractedRate : Optional [float]
    DiscountedCashPrice : Optional [float]
    AetnaBetterHealthMedicaidHMO : Optional [float]
    AetnaCommercialHMOPOS : Optional [float]
    AetnaCommercialPPOOpenAccess : Optional [float]
    AetnaMedicaidHMO : Optional [float]
    AetnaMedicareAdvantageHMO : Optional [float]
    AetnaMedicareMedicareAdvantageHMO : Optional [float]
    AmbetterMedicaidHMO : Optional [float]
    BCBSCommercialHMOPOS : Optional [float]
    BlueCrossBlueShieldCommercialHMOPOS : Optional [float]
    BlueCrossBlueShieldCommercialPPOOpenAccess : Optional [float]
    BlueCrossBlueShieldIPACommercialHMOPOS : Optional [float]
    BlueCrossBlueShieldMedicaidMedicaidHMO : Optional [float]
    BlueCrossBlueShieldMedicareMedicareAdvantageHMO : Optional [float]
    CignaCommercialHMOPOS : Optional [float]
    CignaCommercialPPOOpenAccess : Optional [float]
    CignaMedicareAdvantageHMO : Optional [float]
    CountyCareMedicaidHMO : Optional [float]
    GEHACommercialHMOPOS : Optional [float]
    GenericCommercialother : Optional [float]
    HumanaCommercialHMOPOS : Optional [float]
    HumanaCommercialHMOPOS2nd : Optional [float]
    HumanaCommercialPPOOpenAccess : Optional [float]
    HumanaMedicareMedicareAdvantageHMO : Optional [float]
    IllinicareMedicaidHMO : Optional [float]
    MedicaidHMOOutofState : Optional [float]
    MedicaidMedicaid : Optional [float]
    MedicareAdvantageHMO : Optional [float]
    MedicareMedicare : Optional [float]
    MeridianMedicaidHMO : Optional [float]
    MolinaMedicaidHMO : Optional [float]
    OptumCommercialPPOOpenAccess : Optional [float]
    PhysiciansMutualCommercialother : Optional [float]
    TricareCommercialHMOPOS : Optional [float]
    Type : str
    UHCCommercialother : Optional [float]
    UMRCommercialPPOOpenAccess : Optional [float]
    UMRCommercialPPOOpenAccess2nd : Optional [float]
    UnitedHealhCareCommercialOther : Optional [float]
    UnitedHealthCareCommercialHMOPOS : Optional [float]
    UnitedHealthCareCommercialPPOOpenAccess : Optional [float]
    UnitedHealthCareMedicaidMedicaidHMO : Optional [float]
    UnitedHealthCareMedicaidMedicaidHMO2nd : Optional [float]
    UnitedHealthCareMedicareAdvantageHMO : Optional [float]
    UnitedHealthCareMedicareMedicareAdvantageHMO : Optional [float]
    WellcareMedicareMedicareAdvantageHMO : Optional [float]
    WorkersComp : Optional [float]

class NorthshoreCharges(BaseModel):
    SystemID :  Optional [int]
    LocationName :  Optional [int ]
    InternalCode :  Optional [str]
    ServiceDecsription :  Optional [str ]
    BillingCode :  Optional [str]
    GrossCharge : Optional [float]
    BlueCrossBlueShieldOP : Optional [float]
    BlueCrossBlueShieldIP : Optional [float]
    AetnaOP : Optional [float]
    AetnaIP : Optional [float]
    UnitedHealthcareOP : Optional [float]
    UnitedHealthcareIP : Optional [float]
    CignaOP : Optional [float]
    CignaIP : Optional [float]
    HumanaOP : Optional [float]
    HumanaIP : Optional [float]
    MedicareMedicareAdvantageOP : Optional [float]
    MedicareMedicareAdvantageIP : Optional [float]
    MedicaidMedicaidMCOOP : Optional [float]
    MedicaidMedicaidMCOIP : Optional [float]
    DiscountedCashPrice : Optional [float]
    DeidentifiedMaximumCharge : Optional [float]
    DeidentifiedMinimumCharge : Optional [float]



class NorthwesternCharges(BaseModel):
    LocationID : Optional  [int]
    SystemID : Optional  [int]
    LocationName : Optional  [str]
    BillingCode : Optional  [str]
    ServiceDescription : Optional  [str]
    RevenueCode : Optional  [str]
    GrossCharge : Optional [float]
    DeidentifiedMinimumCharge : Optional [float]
    DeidentifiedMaximumCharge : Optional [float]
    DiscountedCashPrice : Optional [float]
    AETNA509 : Optional [float]
    AETNAAPCN_SP729 : Optional [float]
    AETNABP760 : Optional [float]
    AETNAILPREFERRED139 : Optional [float]
    BCBSBLUECHOICEOPTIONS727 : Optional [float]
    BCBSBLUECHOICEPREFERRED479 : Optional [float]
    BCBSPAR_INDEMNITYADP505 : Optional [float]
    BCBSPPO424 : Optional [float]
    CIGNAALTERNATIVE668 : Optional [float]
    CIGNABROAD667 : Optional [float]
    CIGNAPLUSNM682 : Optional [float]
    HUMANAHMO299 : Optional [float]
    HUMANAPPO145 : Optional [float]
    UHCCORE346 : Optional [float]
    UHCHMO_PPO535 : Optional [float]
    ChargeCode : Optional [float]
    

class RushCharges(BaseModel):
    locationID : Optional [int]
    SystemID : Optional [int]
    LocationName : Optional [str]
    Type :  Optional [str]
    CodeType : Optional [str]
    DefaultCodeID : Optional [str ]
    BillingCode : Optional [str]
    NDC : Optional [str]
    ServiceDescription : Optional [str]
    GrossCharge : Optional [float]
    DeidentifiedMinimumCharge : Optional [float]
    DeidentifiedMaximumCharge : Optional [float]
    DiscountedCashPrice : Optional [float]
    AetnaSignatureAdministratos501021 : Optional [float]
    AetnaStateOfIllinoisPPOHMOOAP501110 : Optional [float]
    ALLIEDBENEFITAETNASIGNATURE501025 : Optional [float]
    BASICPREMIERRUSHEMPALLEGIANCEGWHCIGNA517020 : Optional [float]
    BLUECHOICEHMOBCOFILLINOIS510131 : Optional [float]
    BLUECHOICEPPOBCOFILLINOIS510144 : Optional [float]
    BLUECHOICEOPTIONSBCOBLUEOPTIONSPPO510141 : Optional [float]
    BLUEPRECISIONBCHMOI510143 : Optional [float]
    CIGNACTAEMPLOYEES517025 : Optional [float]
    CIGNAONEHEALTHHMO517030 : Optional [float]
    CORESOURCEAETNASIGNATURE501028 : Optional [float]
    GOLDENRULEUNITEDHEALTHCARE582023 : Optional [float]
    HMOAETNAOPENACCESS501010 : Optional [float]
    HMOOUTOFSTATEBC510016 : Optional [float]
    HMONETWORKCIGNA517010 : Optional [float]
    HMOHUMANA540013 : Optional [float]
    HMOIBLUECROSS510134 : Optional [float]
    OXFORDUNITEDHEALTHCARE582024 : Optional [float]
    POSCHOICEHUMANA540022 : Optional [float]
    POSEPOAETNA501013 : Optional [float]
    POSPOSPLUSCIGNA517013 : Optional [float]
    PPOAETNA501014 : Optional [float]
    PPOANTHEMBC510025 : Optional [float]
    PPOFIRSTHEALTH526010 : Optional [float]
    PPOHFN10536010 : Optional [float]
    PPOHUMANA540015 : Optional [float]
    PPOILLINOISBC510133 : Optional [float]
    PPOMERITAIN631010 : Optional [float]
    PPOMULTIPLAN555710 : Optional [float]
    PPOOUTOFSTATEBC510018 : Optional [float]
    PPOPHCS563012 : Optional [float]
    PPOUNITEDHEALTHCARECHOICESELECTOPTION582010 : Optional [float]
    PPOEPOOPENACCESSNETWORKPLUSCIGNA517012 : Optional [float]
    PPOOPENACCESSPLUSGREATWESTGWHCIGNA532012 : Optional [float]
    SELECTEPORUSHEMPLOYEEALLEGIANCEGWHCIGNA5170 : Optional [float]
    STUDENTRESOURCESPPOUNITEDHEALTHCARE582027 : Optional [float]
    UHCAFFILIATES582025 : Optional [float]
    UMRUNITEDHEALTHCARE582022 : Optional [float]
    UNITEDCORENAVIGATE582021 : Optional [float]
    BASICPREMIERRUSHEMPALLEGIANCEGWHCIGNA517020 : Optional [float]
    BLUECHOICEOPTIONSBCOBLUEOPTIONSPPO5101413 : Optional [float]
    PPOUNITEDHEALTHCARECHOICESELECTOPTION582010 : Optional [float]
    PPOEPOOPENACCESSNETWORKPLUSCIGNA5170125 : Optional [float]
    SELECTEPORUSHEMPLOYEEALLEGIANCEGWHCIGNA5170 : Optional [float]
    UNITEDHEALTHCARECATERPILLARINC582097 : Optional [float]
    AFFILIATESCIGNA517026 : Optional [float]
    BLUECAREDIRECTBCHMOI510142 : Optional [float]
    GENERICIPAHMOIBLUECROSS545010 : Optional [float]
    HMOANTHEMBC510024 : Optional [float]
    HMONETWORKCIGNA5170107 : Optional [float]
    MAILHANDLERSAETNA501044 : Optional [float]
    PPOAETNAILLINOISPREFERRED501032 : Optional [float]
    PPOOPENACCESSPLUSGREATWESTGWHCIGNA5320122 : Optional [float]
    TRANSPLANTHMOPPOAETNA501016 : Optional [float]
    AETNAINTERNATIONAL501036 : Optional [float]
    BDCTBLUEDISTINCTIONCENTERSFORTRANSPLANT5100 : Optional [float]
    CIGNABEHAVIORALHEALTH517022 : Optional [float]
    SPECIALTYPHYSICIANSOFILLINOIS578110 : Optional [float]
    TRANSPLANTCIGNAPPOLIFESOURCE517016 : Optional [float]
    UNIONHEALTHSERVICE581010 : Optional [float]
    
    
    

class UCMCCharges(BaseModel):
    LocationID :  Optional [int]
    SystemID :  Optional [int]
    LocationName :  Optional [str]
    CodeID :  Optional [str]
    DefaultItemCode :  Optional [str]
    ServiceDescription :  Optional [str] 
    CDM_Revenue_Code :  Optional [str]
    BillingCode :  Optional [str]
    CDM_Modifier :  Optional [str]
    grossCharge : Optional [float]
    discountedCashPrice : Optional [float]
    FSC_75_Price : Optional [float]
    FSC_75_Discounted_Cash_Price : Optional [float]
    FSC_171_Price : Optional [float]
    FSC_171_Discounted_Cash_Price : Optional [float]
    FSC_179_Price : Optional [float]
    FSC_179_Discounted_Cash_Price : Optional [float]
    FSC_178_Price : Optional [float]
    FSC_178_Discounted_Cash_Price : Optional [float]
    FSC_176_Price : Optional [float]
    FSC_176_Discounted_Cash_Price : Optional [float]
    FSC_174_Price : Optional [float]
    FSC_174_Discounted_Cash_Price : Optional [float]
    FSC_172_Price : Optional [float]
    FSC_172_Discounted_Cash_Price : Optional [float]
    FSC_70_Price : Optional [float]
    FSC_70_Discounted_Cash_Price : Optional [float]
    FSC_73_Price : Optional [float]
    FSC_73_Discounted_Cash_Price : Optional [float]
    FSC_77_Price : Optional [float]
    FSC_77_Discounted_Cash_Price : Optional [float]
    FSC_170_Price : Optional [float]
    FSC_170_Discounted_Cash_Price : Optional [float]
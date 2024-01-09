https://smithtech.io/api/systems : This endpoint is a reference table containing the system names and ID for the hospital systems. It should be use whenever a SystemID is needed to be passed into another route

https://smithtech.io/api/systems/<int: SystemID> : # Example: Use an actual system_id that exists in your database.

https://smithtech.io/api/systems/4 :

https://smithtech.io/api/locations : This endpoint is a reference table containing the location names and ID for the hospital systems. It should be use whenever a LocationID is needed to be passed into another route

https://smithtech.io/api/locations/<int: SystemID> : Refers to the locations by a specific SystemID

https://smithtech.io/api/locations/1 : Example use for location for SystemID = 1

https://smithtech.io/api/charges/system/<int: SystemID>/location/<int: LocationID> : Returns a table for all the charges at system 4 and location 27

https://smithtech.io/api/charges/system/4/location/27 : Returns a table for all the charges at system 4 and location 27

https://smithtech.io/react/eligibility/insurances : This endpoint is a reference table containing the insurance plan names and ID for the hospital systems. It should be use whenever a PlanID needed to be passed into another route

https://smithtech.io/react/eligibility/insurances/<int: PlanID> : Returns the plan information for given PlanID

https://smithtech.io/react/eligibility/insurances/1 : Example use returning CarrierID,CarrierName,InsuranceTypeID, PlanID,PlanN
https://smithtech.io/react/eligibility/insurance-types : This endpoint is a reference table containing the insurance type names and ID for the hospital systems. It should be use whenever a InsuranceTypeID needed to be passed into another route

https://smithtech.io/react/eligibility/insurance-types/<int: InsuranceTypeID> : returns information regarding a specific InsuranceTypeID, returns InsuranceTypeID and InsuranceType

https://smithtech.io/react/eligibility/insurance-types/1 : #example use passing InsuranceTypeID

https://smithtech.io/react/eligibility/insurance-plans/<int: CarrierID> : This route returns the all of the plans for a specific carrierreturns list of plans with CarrierID,CarrierName,InsuranceTypeID, PlanID, PlanName

https://smithtech.io/react/eligibility/insurance-plans/1 : Example use returns eligible SystemID and LocationID for a given planID

https://smithtech.io/react/eligibility/records/system/<int: SystemID> : Returns in-network plans for a given SystemID

https://smithtech.io/react/eligibility/records/system/4 : Returns in-network providers for a specific SystemID

https://smithtech.io/react/eligibility/records/system/<int: SystemID>/location/<int: LocationID> : Returns in-network providers for a specific SystemID and LocationID

https://smithtech.io/react/eligibility/records/system/4/location/17 : Returns in-network providers for LocationID =17 and SystemID =4

https://smithtech.io/react/eligibility/network-info/<int: PlanID> : Returns in-network plan list for a specific PlanID

https://smithtech.io/react/eligibility/network-info/1 : Returns list of in network locations for given PlanID, returns
a list of LocationID and SystemID

https://smithtech.io/db_admin/tables : Returns all the table in the database

https://smithtech.io/db_admin/columns/HospitalSystem : Refrences the columsn in the Hospital System table

https://smithtech.io/db_admin/columns/HospitalLocation : Refrences the columsn in the HospitalLocation table

https://smithtech.io/db_admin/columns/Charges_Northwestern : Refrences the columsn in the Charges_Northwestern table

https://smithtech.io/db_admin/columns/Charges_LoyolaCDM : Refrences the columsn in the Charges_LoyolaCDM table

https://smithtech.io/db_admin/columns/Charges_NorthShore : Refrences the columsn in the Charges_NorthShore table

https://smithtech.io/db_admin/columns/Charges_Rush : Refrences the columsn in the Charges_Rush table

https://smithtech.io/db_admin/columns/Charges_UCMC :
Refrences the columsn in the Charges_UCMC table

https://smithtech.io/db_admin/columns/Charges_Advocate : Refrences the columsn in the Charges_Advocate table

https://smithtech.io/react/charges/billingcode/<string: BillingCode> : Searches all charges tables for a BillingCode like "%{BillingCode}%"

https://smithtech.io/react/charges/billingcode/99212 : is an exmaple of the use that find all charges where the code is like 99212

https://smithtech.io/react/charges/description/<string: description> : Searches all charges tables for a ServiceDescription like "%{description}%"

https://smithtech.io/react/charges/description/lung : is an exmaple of the use that find all charges where lung is in the description/
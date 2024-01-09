'https://smithtech.io/api/systems', This endpoint is a reference table containing the system names and ID for the hospital systems. It should be use whenever a SystemID is needed to be passed into another route
'https://smithtech.io/api/systems/4', # Example: Use an actual system_id that exists in your database.
'https://smithtech.io/api/locations',This endpoint is a reference table containing the location names and ID for the hospital systems. It should be use whenever a LocationID is needed to be passed into another route
'https://smithtech.io/api/locations/1', # Example: Use an actual system_id that exists in your database.
'https://smithtech.io/api/charges/system/4/location/27', # Example: Use actual system_id and location_id values, returns a large table of charges for a specific SystemID and LocationID
'https://smithtech.io/react/eligibility/carriers',This endpoint is a reference table containing the carrier names and ID for the hospital systems. It should be use whenever a CarrierIDis needed to be passed into another route
'https://smithtech.io/react/eligibility/carriers/1', #Example use
'https://smithtech.io/react/eligibility/insurances',This endpoint is a reference table containing the insurance plan names and ID for the hospital systems. It should be use whenever a PlanID needed to be passed into another route
'https://smithtech.io/react/eligibility/insurances/1',
'https://smithtech.io/react/eligibility/insurance-types',This endpoint is a reference table containing the insurance type names and ID for the hospital systems. It should be use whenever a InsuranceTypeID needed to be passed into another route
'https://smithtech.io/react/eligibility/insurance-types/1', #example use passing InsuranceTypeID
'https://smithtech.io/react/eligibility/insurance-info/carrier/1', example use passing CarrierID
'https://smithtech.io/react/eligibility/insurance-plans/1', This route returns the all of the plans for a specific carrier
'https://smithtech.io/react/eligibility/records/system/1', Returns in network providers for a specific SystemID
'https://smithtech.io/react/eligibility/records/system/4/location/17', Returns in network providers for a specific SystemID and locationID
'https://smithtech.io/react/eligibility/network-info/1',Returns in network providers for a specific PlanID
'https://smithtech.io/db_admin/tables', returns
'https://smithtech.io/db_admin/columns/HospitalSystem', Refrences the columsn in the Hospital System table
'https://smithtech.io/db_admin/columns/HospitalLocation', Refrences the columsn in the HospitalLocation table
'https://smithtech.io/db_admin/columns/Charges_Northwestern', Refrences the columsn in the Charges_Northwestern table
'https://smithtech.io/db_admin/columns/Charges_LoyolaCDM', Refrences the columsn in the Charges_LoyolaCDM table
'https://smithtech.io/db_admin/columns/Charges_NorthShore', Refrences the columsn in the Charges_NorthShore table
'https://smithtech.io/db_admin/columns/Charges_Rush', Refrences the columsn in the Charges_Rush table
'https://smithtech.io/db_admin/columns/Charges_UCMC', Refrences the columsn in the Charges_UCMC table
'https://smithtech.io/db_admin/columns/Charges_Advocate', Refrences the columsn in the Charges_Advocate table

from backend.models.HospitalSystem import HospitalSystem
from backend.models.HospitalLocation import HospitalLocation
from backend.models.Charges_Advcoate import AdvocateCharges
from backend.models.Charges_LoyolaCDM import LoyolaCDMCharges
from backend.models.Charges_Loyola import LoyolaCharges
from backend.models.Charges_Northshore import NorthshoreCharges
from backend.models.Charges_Northwestern import NorthwesternCharges
from backend.models.Charges_Rush import RushCharges
from backend.models.Charges_UCMC import UCMCCharges
from backend.models.Elig_Northwestern import Eligible_Insurance
from backend.models.InsurancePlan import Insurance_Plan
from backend.models.InsuranceTypes import Insurance_Type

from pydantic import ValidationError 
from backend.database.db_helpers import get_insurance_types,get_insurances_by_system_id,  get_insurance_plans, get_charge_data, get_all_insurance_types, get_eligibility_by_year, get_insurance_plan_details, get_charge_data_by_system_id,get_table_data, get_available_locations, get_locations_by_system_id ,get_charge_data_by_location_id, get_location_details
from flask import Blueprint, jsonify, request   
from logs.custom_logger import get_api_logger


charge_models_mapping = {
    1: AdvocateCharges,
    2: LoyolaCDMCharges,
    3: NorthshoreCharges,
    4: NorthwesternCharges,
    5: RushCharges,
    6: UCMCCharges
}

System_ID_Mapping_Table =  {
    1:'Elig_Advocate',
    2:'Elig_Loyola',
    3:'Elig_Northshore',
    4:'Elig_Northwestern',
    5:'Elig_UCMC',
}


api_logger = get_api_logger()
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/systems', methods=['GET'])
def get_systems():
    api_logger.info("Fetching all systems.")
    systems_data = get_table_data("HospitalSystem")  # Assuming 'HospitalInfo' is the schema name
    systems = [HospitalSystem(**system).dict() for system in systems_data]
    return jsonify(systems)

@api.route('/systems/<int:system_id>', methods=['GET'])
def get_system(system_id):
    api_logger.info(f"Fetching system with ID: {system_id}")
    systems_data = get_table_data("HospitalSystem")
    system = next((HospitalSystem(**sys).dict() for sys in systems_data if sys['SystemID'] == system_id), None)
    if system:
        return jsonify(system)
    else:
        api_logger.error(f"System with ID {system_id} not found.")
        return jsonify({"error": "System not found"}), 404

@api.route('/locations', methods=['GET'])
def get_locations():
    api_logger.info("Fetching all locations.")
    locations_data = get_table_data("HospitalLocation")  # Assuming 'HospitalInfo' is the schema name
    locations = [HospitalLocation(**location).dict() for location in locations_data]
    return jsonify(locations)

@api.route('/locations/<int:system_id>', methods=['GET'])
def get_locations_by_system(system_id):
    api_logger.info(f"Fetching locations for system ID: {system_id}")
    locations_data = get_locations_by_system_id(system_id)
    locations = [HospitalLocation(**location).dict() for location in locations_data]
    return jsonify(locations)


@api.route('/charges/system/<int:system_id>/location/<int:location_id>', methods=['GET'])
def get_charges_by_location(system_id, location_id):
    api_logger.info(f"Fetching charges for system ID: {system_id}, location ID: {location_id}")
    
    charge_data, columns = get_charge_data(system_id, location_id)
    
    if charge_data:
        return jsonify({"data": charge_data, "columns": columns})
    else:
        api_logger.error(f"No charge data found for system ID: {system_id}, location ID: {location_id}")
        return jsonify({"error": "Charge data not found for the given system and location ID"}), 404


@api.route('/locations/details/location/<int:location_id>', methods=['GET'])
def get_location_information(location_id):
    api_logger.info(f"Fetching location information for location ID: {location_id}")

    location_details = get_location_details(location_id)
    
    if location_details:
        return jsonify(location_details)
    else:
        api_logger.error(f"Location not found for location ID: {location_id}")
        return jsonify({"error": "Location not found"}), 404



@api.route('/insurances/plans/plan/<int:plan_id>', methods=['GET'])
def insurance_plan_details(plan_id):
    api_logger.info(f"Fetching insurance plan details for plan ID: {plan_id}")

    plan_details = get_insurance_plan_details(plan_id)
    
    if plan_details:
        try:
            insurance_plan = Insurance_Plan(**plan_details)
            return jsonify(insurance_plan.dict())
        except ValidationError as e:
            api_logger.error(f"Data validation error for insurance plan details: {e}")
            return jsonify({"error": "Invalid data format"}), 500
    else:
        api_logger.error(f"Insurance plan not found for plan ID: {plan_id}")
        return jsonify({"error": "Insurance plan not found"}), 404


@api.route('/insurances/types', methods=['GET'])
def insurance_types():
    api_logger.info("Fetching all insurance types")
    types = get_all_insurance_types()

    try:
        return jsonify([Insurance_Type(**type_).dict() for type_ in types])
    except ValidationError as e:
        api_logger.error(f"Data validation error for insurance types: {e}")
        return jsonify({"error": "Invalid data format"}), 500




@api.route('/insurances/eligibility', methods=['GET'])
def eligibility_by_year():
    year = request.args.get('year', type=int)
    api_logger.info(f"Fetching insurance eligibility for year: {year}")

    if year:
        eligibility_list = get_eligibility_by_year(year)
        try:
            return jsonify([Insurance_Type(**item).dict() for item in eligibility_list])
        except ValidationError as e:
            api_logger.error(f"Data validation error for eligibility by year: {e}")
            return jsonify({"error": "Invalid data format"}), 500
    else:
        api_logger.error("Year parameter is required for insurance eligibility")
        return jsonify({"error": "Year parameter is required"}), 400


# Add this to api_routes.py

@api.route('/insurances/system/<int:system_id>', methods=['GET'])
def get_insurances_by_system(system_id):
    api_logger.info(f"Fetching insurances for system ID: {system_id}")
    
    # Fetch insurances by system_id using the helper function
    insurances = get_insurances_by_system_id(system_id)
    
    if insurances:
        # Convert the list of dictionaries to a list of Insurance_Plan Pydantic models
        insurance_models = [Insurance_Plan(**insurance) for insurance in insurances]
        return jsonify([insurance_model.dict() for insurance_model in insurance_models])
    else:
        # Log an error and send a 404 response if no data was found
        api_logger.error(f"No insurance data found for system ID: {system_id}")
        return jsonify({"error": "No insurance data found for the given system ID"}), 404

@api.route('/insurances/plans', methods=['GET'])
def get_insurance_plans_route():
    api_logger.info("Fetching all insurance plans.")
    
    insurance_plans_data = get_insurance_plans()
    insurance_plans = [Insurance_Plan(**plan).dict() for plan in insurance_plans_data]
    
    return jsonify(insurance_plans)

@api.route('/insurances/types', methods=['GET'])
def get_insurance_types_route():
    api_logger.info("Fetching all insurance types.")
    try:
        insurance_types_data = get_insurance_types()
        insurance_types = [Insurance_Type(**type_data).dict() for type_data in insurance_types_data]
        return jsonify(insurance_types)
    except ValidationError as e:
        api_logger.error(f"Data validation error for insurance types: {e}")
        return jsonify({"error": "Invalid data format"}), 500
    except Exception as e:
        api_logger.error(f"An error occurred while fetching insurance types: {e}")
        return jsonify({"error": "An error occurred"}), 500
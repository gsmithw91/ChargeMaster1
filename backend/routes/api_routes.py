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
from backend.database.db_helpers import get_carrier_by_id, get_all_carriers , get_all_insurance_plans,get_in_network_eligibility, get_system_by_id,get_insurance_types,get_insurances_by_system_id,  get_insurance_plans, get_charge_data, get_insurance_plan_details, get_filtered_data, get_locations_by_system_id , get_location_details
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
    try:
        # Here we call 'get_filtered_data' with just the table name since no filters are needed
        systems_data = get_filtered_data("HospitalSystem")
        systems = [HospitalSystem(**system).dict() for system in systems_data]
        return jsonify(systems)
    except ValidationError as e:
        api_logger.error(f"Data validation error for systems: {e}")
        return jsonify({"error": "Invalid data format"}), 500
    except Exception as e:
        api_logger.error(f"An error occurred while fetching systems: {e}")
        return jsonify({"error": "An error occurred"}), 500



@api.route('/systems/<int:system_id>', methods=['GET'])
def get_system(system_id):
    api_logger.info(f"Fetching system with ID: {system_id}")
    system_data = get_system_by_id(system_id)
    if system_data:
        return jsonify(HospitalSystem(**system_data).dict())
    else:
        api_logger.error(f"System with ID {system_id} not found.")
        return jsonify({"error": "System not found"}), 404


@api.route('/locations', methods=['GET'])
def get_all_locations():
    api_logger.info("Fetching all locations.")
    try:
        # Use get_filtered_data to fetch all locations
        locations_data = get_filtered_data("HospitalLocation")
        locations = [HospitalLocation(**location).dict() for location in locations_data]
        return jsonify(locations)
    except ValidationError as e:
        api_logger.error(f"Data validation error for locations: {e}")
        return jsonify({"error": "Invalid data format"}), 500
    except Exception as e:
        api_logger.error(f"An error occurred while fetching locations: {e}")
        return jsonify({"error": "An error occurred"}), 500


@api.route('/locations/<int:system_id>', methods=['GET'])
def get_locations_by_system(system_id):
    api_logger.info(f"Fetching locations for system ID: {system_id}")
    try:
        # Use get_locations_by_system_id to fetch locations filtered by system_id
        locations_data = get_locations_by_system_id(system_id)
        locations = [HospitalLocation(**location).dict() for location in locations_data]
        return jsonify(locations)
    except ValidationError as e:
        api_logger.error(f"Data validation error for locations with system ID {system_id}: {e}")
        return jsonify({"error": "Invalid data format"}), 500
    except Exception as e:
        api_logger.error(f"An error occurred while fetching locations for system ID {system_id}: {e}")
        return jsonify({"error": "An error occurred"}), 500



@api.route('/insurances/plans', methods=['GET'])
def get_all_insurance_plans_route():
    api_logger.info("Fetching all insurance plans")
    try:
        plans = get_all_insurance_plans()  # Call the function that actually fetches the plans
        return jsonify([Insurance_Plan(**plan).dict() for plan in plans])
    except ValidationError as e:
        api_logger.error(f"Data validation error for insurance plans: {e}")
        return jsonify({"error": "Invalid data format"}), 500
    except Exception as e:
        api_logger.error(f"An unexpected error occurred while fetching insurance plans: {e}")
        return jsonify({"error": "An error occurred"}), 500



@api.route('/insurances/plan-types', methods=['GET'])
def insurance_plan_types():
    api_logger.info("Fetching all insurance types")
    types = get_insurance_types()

    try:
        return jsonify([Insurance_Type(**type_).dict() for type_ in types])
    except ValidationError as e:
        api_logger.error(f"Data validation error for insurance types: {e}")
        return jsonify({"error": "Invalid data format"}), 500


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





@api.route('/eligibility/in-network/<int:system_id>', methods=['GET'])
def get_in_network_eligibility_route(system_id):
    try:
        api_logger.info(f"Fetching in-network eligibility for system ID: {system_id}")
        eligibility_data = get_in_network_eligibility(system_id)
        return jsonify(eligibility_data)
    except Exception as e:
        api_logger.error(f"An error occurred while fetching in-network eligibility for system ID {system_id}: {e}")
        return jsonify({"error": "An error occurred"}), 500

@api.route('/charges', defaults={'system_id': None, 'location_id': None}, methods=['GET'])
@api.route('/charges/system/<int:system_id>', defaults={'location_id': None}, methods=['GET'])
@api.route('/charges/system/<int:system_id>/location/<int:location_id>', methods=['GET'])
def get_charges(system_id, location_id):
    api_logger.info(f"Fetching charges for system ID: {system_id or 'all'}, location ID: {location_id or 'all'}")

    try:
        charge_data, columns = get_charge_data(system_id, location_id)
        if charge_data:
            return jsonify({"data": charge_data, "columns": columns})
        else:
            api_logger.error(f"No charge data found for system ID: {system_id or 'all'}, location ID: {location_id or 'all'}")
            return jsonify({"error": "Charge data not found"}), 404
    except Exception as e:
        api_logger.error(f"An unexpected error occurred while fetching charge data: {e}")
        return jsonify({"error": str(e)}), 500


@api.route('/carriers', methods=['GET'])
def get_carriers():
    api_logger.info("Fetching all carriers.")
    try:
        carriers = get_all_carriers()
        return jsonify(carriers)
    except Exception as e:
        api_logger.error(f"An error occurred while fetching carriers: {e}")
        return jsonify({"error": "An error occurred"}), 500

@api.route('/carriers/<int:carrier_id>', methods=['GET'])
def get_carrier(carrier_id):
    api_logger.info(f"Fetching carrier with ID: {carrier_id}")
    try:
        carrier = get_carrier_by_id(carrier_id)
        if carrier:
            return jsonify(carrier)
        else:
            api_logger.error(f"Carrier with ID {carrier_id} not found.")
            return jsonify({"error": "Carrier not found"}), 404
    except Exception as e:
        api_logger.error(f"An error occurred while fetching the carrier: {e}")
        return jsonify({"error": "An error occurred"}), 500


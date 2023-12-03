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
from pydantic import ValidationError 
from backend.database.db_helpers import search_in_network_insurance, get_in_network_insurance, get_all_insurance_types, get_eligibility_by_year, get_insurance_plan_details,get_in_network_insurance, get_charge_data_by_system_id,get_table_data, get_available_locations, get_locations_by_system_id ,get_charge_data_by_location_id, get_location_details
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


@api.route('/charges/system/<int:system_id>', methods=['GET'])
def get_charges_by_system(system_id):
    api_logger.info(f"Fetching charges for system ID: {system_id}")
    
    charge_data, columns = get_charge_data_by_system_id(system_id)
    
    if not columns:
        api_logger.error(f"No charge table found for system ID: {system_id}")
        return jsonify({"error": "Charge table not found for the given system ID"}), 404

    if charge_data:
        return jsonify({"data": charge_data, "columns": columns})
    else:
        api_logger.error(f"Charge data not found for system ID: {system_id}")
        return jsonify({"error": "Charge data not found for the given system ID"}), 404


@api.route('/charges/location/<int:system_id>/<int:location_id>', methods=['GET'])
def get_charges_by_location(system_id, location_id):
    api_logger.info(f"Fetching charges for system ID: {system_id}, location ID: {location_id}")
    
    charge_data, columns = get_charge_data_by_location_id(system_id, location_id)
    
    if not columns:
        api_logger.error(f"No charge data found for system ID: {system_id}, location ID: {location_id}")
        return jsonify({"error": "Charge data not found for the given system and location ID"}), 404

    return jsonify({"data": charge_data, "columns": columns})


@api.route('/locations/details/<int:location_id>', methods=['GET'])
def get_location_information(location_id):
    location_details = get_location_details(location_id)
    if location_details:
        return jsonify(location_details)
    else:
        return jsonify({"error": "Location not found"}), 404


@api.route('/in_network_insurance', methods=['GET'])
def in_network_insurance():
    location_id = request.args.get('location_id', default=None, type=int)
    results = get_in_network_insurance(location_id)
    
    # Create instances of your Pydantic model from the dictionary data
    result_models = [Eligible_Insurance(**result) for result in results]
    
    # Convert the Pydantic model instances to dictionaries
    result_dicts = [model.dict() for model in result_models]
    
    return jsonify(result_dicts)

@api.route('/insurance/plans/<int:plan_id>', methods=['GET'])
def insurance_plan_details(plan_id):
    plan_details = get_insurance_plan_details(plan_id)
    if plan_details:
        return jsonify(plan_details.dict())
    else:
        return jsonify({"error": "Insurance plan not found"}), 404

@api.route('/insurance/types', methods=['GET'])
def insurance_types():
    types = get_all_insurance_types()
    return jsonify([type_.dict() for type_ in types])

@api.route('/insurance/eligibility', methods=['GET'])
def eligibility_by_year():
    year = request.args.get('year', type=int)
    if year:
        eligibility_list = get_eligibility_by_year(year)
        return jsonify([item.dict() for item in eligibility_list])
    else:
        return jsonify({"error": "Year parameter is required"}), 400

@api.route('/insurance/search', methods=['GET'])
def insurance_search():
    query = request.args.get('query', default='', type=str)
    if query:
        search_results = search_in_network_insurance(query)
        return jsonify([result.dict() for result in search_results])
    else:
        return jsonify({"error": "Search query parameter is required"}), 400

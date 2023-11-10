from backend.models.HospitalSystem import HospitalSystem
from backend.models.HospitalLocation import HospitalLocation
from backend.models.Charges_Advcoate import AdvocateCharges
from backend.models.Charges_LoyolaCDM import LoyolaCDMCharges
from backend.models.Charges_Loyola import LoyolaCharges
from backend.models.Charges_Northshore import NorthshoreCharges
from backend.models.Charges_Northwestern import NorthwesternCharges
from backend.models.Charges_Rush import RushCharges
from backend.models.Charges_UCMC import UCMCCharges

from pydantic import ValidationError 
from backend.database.db_helpers import get_charge_data_by_system_id,get_table_data, get_available_locations, get_locations_by_system_id 
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
    systems_data = get_table_data("HospitalSystem")
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
    locations_data = get_table_data("HospitalLocation")
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
    charge_model = charge_models_mapping.get(system_id)
    
    if not charge_model:
        api_logger.error(f"No charge model found for system ID: {system_id}")
        return jsonify({"error": "Charge model not found for the given system ID"}), 404

    charge_data = get_charge_data_by_system_id(system_id, charge_model)
    
    if charge_data:
        return jsonify(charge_data)
    else:
        api_logger.error(f"Charge data not found for system ID: {system_id}")
        return jsonify({"error": "Charge data not found for the given system ID"}), 404

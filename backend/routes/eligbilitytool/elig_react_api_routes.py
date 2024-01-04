from pydantic import ValidationError 
from backend.database.db_helpers import get_insurance_info_by_carrier, get_insurance_type_by_id,get_insurance_by_plan_id, get_column_names_from_table, get_carrier_by_id, get_all_carriers , get_all_insurance_plans,get_in_network_eligibility, get_system_by_id,get_insurance_types, get_insurance_plans, get_charge_data, get_insurance_plan_details, get_filtered_data, get_locations_by_system_id , get_location_details
from backend.database.elig_db_helpers import get_all_elig_records, get_elig_records_by_location
from flask import Blueprint, jsonify, request , url_for, session
from logs.custom_logger import api_logger
import pandas as pd

#Create models for Eligibility response

elig_api = Blueprint('elig_api', __name__, url_prefix='/react/eligibility')



@elig_api.route('/carriers', methods=['GET'])
def get_carrier_JSON():
    """
    Returns a JSON object of all carriers
    """
    api_logger.info('Getting all carriers')
    carriers = get_all_carriers()
    return jsonify(carriers)



@elig_api.route('/carriers/<int:carrier_id>', methods=['GET'])
def get_carrier(carrier_id):
    """
    Endpoint to get details of a specific carrier by carrier ID.
    """
    api_logger.info(f'Fetching details for carrier ID: {carrier_id}')
    try:
        carrier_details = get_carrier_by_id(carrier_id)
        if carrier_details:
            return jsonify(carrier_details)
        else:
            return jsonify({"error": "Carrier not found"}), 404
    except Exception as e:
        api_logger.error(f"An error occurred while fetching carrier details: {e}")
        return jsonify({"error": "An error occurred while fetching carrier details"}), 500



@elig_api.route('/insurances', methods=['GET'])
def get_insurance_plans_route():
    """
    Endpoint to get insurance plans, optionally filtered by system_id and location_id.
    """
    try:
        system_id = request.args.get('system_id', type=int)  # Convert to int if parameter is present
        location_id = request.args.get('location_id', type=int)  # Convert to int if parameter is present

        api_logger.info(f"Fetching insurance plans for system ID: {system_id} and location ID: {location_id}")
        plans = get_insurance_plans(system_id=system_id, location_id=location_id)

        return jsonify(plans)
    except Exception as e:
        api_logger.error(f"An error occurred while fetching insurance plans: {e}")
        return jsonify({"error": "An error occurred while fetching insurance plans"}), 500



@elig_api.route('/insurances/<int:plan_id>', methods=['GET'])
def get_insurance_plan(plan_id):
    """
    Endpoint to get details of an insurance plan by plan ID.
    """
    api_logger.info(f'Fetching insurance plan details for Plan ID: {plan_id}')
    try:
        plan_details = get_insurance_by_plan_id(plan_id)
        if plan_details:
            return jsonify(plan_details)
        else:
            return jsonify({"error": "Insurance plan not found"}), 404
    except Exception as e:
        api_logger.error(f"An error occurred while fetching insurance plan details: {e}")
        return jsonify({"error": "An error occurred while fetching insurance plan details"}), 500




@elig_api.route('/insurance-types', methods=['GET'])
def get_insurance_types_route():
    """
    Endpoint to get all insurance types.
    """
    api_logger.info('Fetching all insurance types')
    try:
        insurance_types = get_insurance_types()
        return jsonify(insurance_types)
    except Exception as e:
        api_logger.error(f"An error occurred while fetching insurance types: {e}")
        return jsonify({"error": "An error occurred while fetching insurance types"}), 500
    



@elig_api.route('/insurance-types/<int:insurance_type_id>', methods=['GET'])
def get_insurance_type(insurance_type_id):
    """
    Endpoint to get details of a specific insurance type by insurance type ID.
    """
    api_logger.info(f'Fetching details for insurance type ID: {insurance_type_id}')
    try:
        insurance_type_details = get_insurance_type_by_id(insurance_type_id)
        if insurance_type_details:
            return jsonify(insurance_type_details)
        else:
            return jsonify({"error": "Insurance type not found"}), 404
    except Exception as e:
        api_logger.error(f"An error occurred while fetching insurance type details: {e}")
        return jsonify({"error": "An error occurred while fetching insurance type details"}), 500




@elig_api.route('/insurance-info/carrier/<int:carrier_id>', methods=['GET'])
def get_insurance_info(carrier_id):
    """
    Endpoint to get insurance information for a specific carrier.
    """
    api_logger.info(f'Fetching insurance info for Carrier ID: {carrier_id}')
    try:
        insurance_info = get_insurance_info_by_carrier(carrier_id)
        if insurance_info:
            return jsonify(insurance_info)
        else:
            return jsonify({"error": "No insurance information found for the specified carrier"}), 404
    except Exception as e:
        api_logger.error(f"An error occurred while fetching insurance information: {e}")
        return jsonify({"error": "An error occurred while fetching insurance information"}), 500


from backend.database.db_helpers import get_insurance_plans_by_carrier_id

@elig_api.route('/insurance-plans/<int:carrier_id>', methods=['GET'])
def get_insurance_plans_for_carrier(carrier_id):
    """
    Endpoint to get insurance plans for a specific carrier.
    """
    insurance_plans = get_insurance_plans_by_carrier_id(carrier_id)
    return jsonify(insurance_plans)



@elig_api.route('/eligibility/all/<int:system_id>', methods=['GET'])
def get_all_eligibility_records(system_id):
    api_logger.info(f'Fetching all eligibility records for system ID: {system_id}')
    try:
        records = get_all_elig_records(system_id)
        return jsonify(records)
    except Exception as e:
        api_logger.error(f"An error occurred while fetching eligibility records: {e}")
        return jsonify({"error": "An error occurred while fetching eligibility records"}), 500


@elig_api.route('/eligibility/filter/<int:system_id>/<int:location_id>', methods=['GET'])
def get_eligibility_records_filtered(system_id, location_id):
    api_logger.info(f"Fetching filtered eligibility records for system ID: {system_id} and location ID: {location_id}")
    try:
        filtered_records = get_elig_records_by_location(system_id, location_id)
        return jsonify(filtered_records)
    except Exception as e:
        api_logger.error(f"An error occurred while fetching filtered eligibility records: {e}")
        return jsonify({"error": "An error occurred while fetching filtered eligibility records"}), 500

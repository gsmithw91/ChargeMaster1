from flask import Blueprint, jsonify, request
from logs.custom_logger import api_logger
from backend.database.chargesheet_helpers import (
    create_user_charge_sheet,
    get_chargesheet_by_user_ID,
    add_charge_to_sheet,
    add_charges_to_sheet,
    get_charge_details_for_user_chargesheet,
    get_charge_info_by_location_and_id,
    delete_user_chargesheet_and_details
    ,get_filtered_charge_sheets
)

chargesheet_api = Blueprint('chargesheet_api', __name__, url_prefix='/react/chargesheet')

def handle_api_error(e, message="An error occurred", status_code=500):
    api_logger.error(f"{message}: {e}")
    return jsonify({'error': str(e)}), status_code

@chargesheet_api.route('/create', methods=['POST'])
def create_chargesheet():
    try:
        user_id = request.json.get('user_id')
        charge_sheet_name_default = request.json.get('charge_sheet_name_default', None)
        charge_sheet_id = create_user_charge_sheet(user_id, charge_sheet_name_default)
        return jsonify({'charge_sheet_id': charge_sheet_id}), 200 if charge_sheet_id else 500
    except Exception as e:
        return handle_api_error(e, "Error creating charge sheet")

@chargesheet_api.route('/list/<int:user_id>', methods=['GET'])
def list_charge_sheets(user_id):
    try:
        charge_sheets = get_chargesheet_by_user_ID(user_id)
        charge_sheets_dicts = [
            {
                'UserChargeSheetID': row.UserChargeSheetID,
                'UserID': row.UserID,
                'CreatedAt': row.CreatedAt,
                'ChargeSheetNameDefault': row.ChargeSheetNameDefault
            } for row in charge_sheets
        ]

        return jsonify({'charge_sheets': charge_sheets_dicts}), 200
    except Exception as e:
        return handle_api_error(e, f"Error fetching charge sheets for user {user_id}")

@chargesheet_api.route('/get_charge_sheet_data/<int:user_id>/<int:user_charge_sheet_id>', methods=['GET'])
def get_charge_sheet_data(user_id, user_charge_sheet_id):
    try:
        charge_sheet_data = get_filtered_charge_sheets(user_id, user_charge_sheet_id)
        
        if not charge_sheet_data:
            return jsonify({'error': 'Charge sheet data not found'}), 404

        return jsonify(charge_sheet_data), 200
    except Exception as e:
        return handle_api_error(e, "Error fetching charge sheet data")

@chargesheet_api.route('/add_charge', methods=['POST'])
def add_charge():
    try:
        data = request.json
        add_charge_to_sheet(data['charge_sheet_id'], data['user_id'], data['location_id'], data['system_id'], data['charge_id'])
        return jsonify({'message': 'Charge added successfully'}), 200
    except KeyError:
        return jsonify({'error': 'Missing required fields'}), 400
    except Exception as e:
        return handle_api_error(e, "Error adding charge")

@chargesheet_api.route('/details/<int:user_id>/<int:charge_sheet_id>', methods=['GET'])
def charge_sheet_details(user_id, charge_sheet_id):
    try:
        details = get_charge_details_for_user_chargesheet(user_id, charge_sheet_id)
        charge_sheet_name_default = details[0].get("ChargeSheetNameDefault", "Unknown") if details else "Unknown"
        return jsonify({'details': details, 'chargeSheetNameDefault': charge_sheet_name_default}), 200
    except Exception as e:
        return handle_api_error(e, "Error fetching charge sheet details")

@chargesheet_api.route('/add_multiple_charges', methods=['POST'])
def add_multiple_charges():
    try:
        data = request.json
        add_charges_to_sheet(data['charge_sheet_id'], data['user_id'], data['charges'])
        return jsonify({'message': 'Charges added successfully'}), 200
    except Exception as e:
        return handle_api_error(e, "Error adding multiple charges")

@chargesheet_api.route('/get_charge_info', methods=['POST'])
def get_charge_info():
    try:
        data = request.json
        if not all(key in data for key in ['system_id', 'location_id', 'charge_id']):
            return jsonify({'error': 'Missing parameters'}), 400

        charge_info = get_charge_info_by_location_and_id(data['system_id'], data['location_id'], data['charge_id'])
        return jsonify({'charge_info': charge_info}), 200 if charge_info else 404
    except Exception as e:
        return handle_api_error(e, "Error getting charge info")

@chargesheet_api.route('/delete/<int:user_id>/<int:user_charge_sheet_id>', methods=['DELETE'])
def delete_chargesheet(user_id, user_charge_sheet_id):
    try:
        if delete_user_chargesheet_and_details(user_id, user_charge_sheet_id):
            return jsonify({'message': 'Charge sheet deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete charge sheet'}), 500
    except Exception as e:
        return handle_api_error(e, "Error deleting charge sheet")

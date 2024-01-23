from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from logs.custom_logger import api_logger
from backend.database.chargesheet_helpers import (
    create_user_charge_sheet,
    get_chargesheet_by_user_ID,
    add_charge_to_sheet,
    add_charges_to_sheet,
    get_charge_details_for_user_chargesheet
)

chargesheet_api = Blueprint('chargesheet_api', __name__, url_prefix='/chargesheet')

@chargesheet_api.route('/create', methods=['POST'])
def create_chargesheet():
    user_id = request.json.get('user_id')
    charge_sheet_id = create_user_charge_sheet(user_id)
    return jsonify({'charge_sheet_id': charge_sheet_id}), 200 if charge_sheet_id else 500

@chargesheet_api.route('/list/<int:user_id>', methods=['GET'])
def list_charge_sheets(user_id):
    try:
        charge_sheets = get_chargesheet_by_user_ID(user_id)
        # Manually construct a list of dictionaries
        charge_sheets_dicts = []
        for row in charge_sheets:
            row_dict = {
                'UserChargeSheetID': row.UserChargeSheetID,
                'UserID': row.UserID,
                # Include other fields as necessary
            }
            charge_sheets_dicts.append(row_dict)

        return jsonify({'charge_sheets': charge_sheets_dicts}), 200
    except Exception as e:
        api_logger.error(f"Error fetching charge sheets for user {user_id}: {e}")
        return jsonify({'error': str(e)}), 500
    
    
@chargesheet_api.route('/add_charge', methods=['POST'])
def add_charge():
    data = request.json
    charge_sheet_id = data['charge_sheet_id']
    user_id = data['user_id']
    location_id = data['location_id']
    system_id = data['system_id']
    charge_id = data['charge_id']
    add_charge_to_sheet(charge_sheet_id, user_id, location_id, system_id, charge_id)
    return jsonify({'message': 'Charge added successfully'}), 200

@chargesheet_api.route('/details/<int:user_id>/<int:charge_sheet_id>', methods=['GET'])
def charge_sheet_details(user_id, charge_sheet_id):
    details = get_charge_details_for_user_chargesheet(user_id, charge_sheet_id)
    return jsonify({'details': details}), 200 if details else 500




@chargesheet_api.route('/add_multiple_charges', methods=['POST'])
def add_multiple_charges():
    data = request.json
    user_charge_sheet_id = data['charge_sheet_id']
    user_id = data['user_id']
    charges = data['charges']  # List of charge details

    try:
        add_charges_to_sheet(user_charge_sheet_id, user_id, charges)
        return jsonify({'message': 'Charges added successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
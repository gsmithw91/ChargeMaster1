from backend.models.HospitalSystem import HospitalSystem
from backend.models.HospitalLocation import HospitalLocation
from backend.models.Charges_models import *
from backend.models.Elig_Northwestern import Eligible_Insurance
from backend.models.InsurancePlan import Insurance_Plan
from backend.models.InsuranceTypes import Insurance_Type

from pydantic import ValidationError 
from backend.database.db_helpers import get_column_names_from_table, get_carrier_by_id, get_all_carriers , get_all_insurance_plans,get_in_network_eligibility, get_system_by_id,get_insurance_types,get_insurances_by_system_id,  get_insurance_plans, get_charge_data, get_insurance_plan_details, get_filtered_data, get_locations_by_system_id , get_location_details
from flask import Blueprint, jsonify, request , url_for, session
from logs.custom_logger import api_logger
import pandas as pd

react_api = Blueprint('react_api', __name__, url_prefix='/react')

charge_models_mapping = {
    1: AdvocateCharges, # a5a7d4
    2: LoyolaCDMCharges, #a30046
    3: NorthshoreCharges, # 2361fd
    4: NorthwesternCharges, # 63599e
    5: RushCharges, # 006937
    6: UCMCCharges # 800000
}


System_ID_Mapping_Table =  {
    1:'Elig_Advocate',
    2:'Elig_Loyola',
    3:'Elig_Northshore',
    4:'Elig_Northwestern',
    5:'Elig_UCMC',
}


@react_api.route('/systems', methods=['GET'])
def get_systems_react():
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
    

@react_api.route('/locations/<int:system_id>', methods=['GET'])
def get_locations_by_system_for_react(system_id):
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





@react_api.route('/charges', defaults={'system_id': None, 'location_id': None}, methods=['GET'])
@react_api.route('/charges/system/<int:system_id>', defaults={'location_id': None}, methods=['GET'])
@react_api.route('/charges/system/<int:system_id>/location/<int:location_id>', methods=['GET'])
def get_charges_for_react(system_id, location_id):
    api_logger.info(f"Received request for charges - System ID: {system_id or 'all'}, Location ID: {location_id or 'all'}")

    try:
        # Log the specific query being executed (if applicable)
        api_logger.info(f"Querying charges data for System ID: {system_id}, Location ID: {location_id}")
        charge_data, _ = get_charge_data(system_id, location_id)

        if charge_data:
            api_logger.info(f"Found charge data for System ID: {system_id}, Location ID: {location_id}")
            return jsonify(charge_data)
        else:
            api_logger.warning(f"No charge data found for System ID: {system_id or 'all'}, Location ID: {location_id or 'all'}")
            return jsonify({"error": "Charge data not found"}), 404
    except Exception as e:
        api_logger.error(f"An unexpected error occurred while fetching charge data: {e}")
        return jsonify({"error": str(e)}), 500





System_ID_Charges_Tables_Mapping = {
    1:'Charges_Advocate',
    2:'Charges_LoyolaIns',
    3:'Charges_Northshore',
    4:'Charges_Northwestern',
    5:'Charges_Rush',
    6:'Charges_UCMC',
}

@react_api.route('/columns/<int:system_id>', methods=['GET'])
def get_columns_for_system(system_id):
    api_logger.info(f"Fetching columns for system ID: {system_id}")

    try:
        table_name = System_ID_Charges_Tables_Mapping.get(system_id)
        if table_name:
            column_names = get_column_names_from_table(table_name)
            if column_names:
                return jsonify({"columns": column_names})
            else:
                return jsonify({"error": "No columns available for the specified table"}), 404
        else:
            return jsonify({"error": "Invalid system ID or table not found"}), 404
    except Exception as e:
        api_logger.error(f"An error occurred while fetching columns: {e}")
        return jsonify({"error": str(e)}), 500

@react_api.route('/chargesheet/process-items', methods=['POST'])
def process_items():
    try:
        # Get the JSON data from the request
        selected_items = request.json

        # Clean up the selected items by removing null, undefined, 0, 0.00, or 0.0 values
        cleaned_items = []
        for item in selected_items:
            cleaned_item = {}
            for key, value in item.items():
                if value is not None and value != 0 and not (
                    isinstance(value, str) and value in {"0", "0.00", "0.0"}
                ):
                    cleaned_item[key] = value
            cleaned_items.append(cleaned_item)

        # Create a DataFrame from the cleaned items
        cleaned_item_df = pd.DataFrame(cleaned_items)

        # Print the head of the DataFrame (first 5 rows) to the console
        print(cleaned_item_df.head().to_json(orient="split"))

        # You can perform further processing or analysis on the DataFrame here

        return jsonify({"message": "Items processed successfully!"})

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

@react_api.route('/chargesheet/download-csv', methods=['POST'])
def download_csv():
    try:
        # Assuming the incoming data is a JSON array
        charge_sheet_items = request.json
        if not isinstance(charge_sheet_items, list):
            return jsonify({"error": "Invalid data format. Expected an array."}), 400

        # Clean up the ChargeSheet items by removing null, undefined, 0, 0.00, or 0.0 values
        cleaned_items = []
        for item in charge_sheet_items:
            cleaned_item = {}
            for key, value in item.items():
                if value is not None and value != 0 and not (
                    isinstance(value, str) and value in {"0", "0.00", "0.0"}
                ):
                    cleaned_item[key] = value
            cleaned_items.append(cleaned_item)

        # Create a DataFrame from the cleaned items
        cleaned_item_df = pd.DataFrame(cleaned_items)

        # Save the cleaned items as a CSV file
        csv_filename = "cleaned_charge_sheet.csv"
        cleaned_item_df.to_csv(csv_filename, index=False)

        # Process the cleaned ChargeSheet items here (optional)

        # You can access the SystemID, LocationID, and ChargeID for each selection in cleaned_items

        # Return the CSV file for download
        return send_file(csv_filename, as_attachment=True)

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500
import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from backend.database.chargesheet_helpers import (
    get_connection_UsersDB,
    test_db_connection,
    create_user_charge_sheet,
    get_chargesheet_by_user_ID,
    add_charge_to_sheet,
    get_charge_details_for_user_chargesheet
)

def run_tests():
    # Test database connection
    print("Testing database connection...")
    test_db_connection()

    # Set a test user ID
    test_user_id = 59

    # Create a new user charge sheet
    print(f"\nCreating a user charge sheet for User ID {test_user_id}...")
    user_charge_sheet_id = create_user_charge_sheet(test_user_id)
    print(f"Created UserChargeSheetID: {user_charge_sheet_id}")

    # Retrieve charge sheets for the user
    print(f"\nRetrieving charge sheets for User ID {test_user_id}...")
    charge_sheets = get_chargesheet_by_user_ID(test_user_id)
    print("Charge sheets:", charge_sheets)

    # Add a charge to the sheet
    for i in range (1,5):
        print(f"\nAdding a charge to the UserChargeSheetID {user_charge_sheet_id}...")
        location_id, system_id, charge_id = i, i, i  # Example IDs
        add_charge_to_sheet(user_charge_sheet_id, test_user_id, location_id, system_id, charge_id)
        print("Charge added to the sheet.")

    # Retrieve updated charge sheets for the user
    print(f"\nRetrieving updated charge sheets for User ID {test_user_id}...")
    updated_charge_sheets = get_chargesheet_by_user_ID(test_user_id)
    print("Updated charge sheets:", updated_charge_sheets)

    # Retrieve charge details for a specific chargesheet
    print(f"\nRetrieving charge details for UserChargeSheetID {user_charge_sheet_id} and User ID {test_user_id}...")
    charge_details = get_charge_details_for_user_chargesheet(test_user_id, user_charge_sheet_id)
    print("Charge details:", charge_details)

if __name__ == "__main__":
    run_tests()

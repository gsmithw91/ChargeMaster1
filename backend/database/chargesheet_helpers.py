# backend/database/login_helpers.py
import pyodbc
import os

# Function to establish a connection to the Users database
def get_connection_UsersDB():
    # Check the environment variable
    app_env = os.getenv('APP_ENV', 'desktop')  # Defaults to 'desktop' if not set
    app_env = 'server'
    if app_env == 'server':
        # Connection string for the server
        conn_str = (
            r"DRIVER={ODBC Driver 18 for SQL Server};" +
            r"SERVER=172.234.28.216;" +  # Replace with your Linode server IP or hostname
            r"DATABASE=ChargeMaster_Users;" +
            r"UID=SA;" +            # Replace with your SQL username
            r"PWD=B90b909021!;" +   # Replace with your SQL password
            r"TrustServerCertificate=yes;"  # This might be optional depending on your setup
        )
    else:
        # Connection string for the desktop
        conn_str = (
            r'DRIVER={ODBC Driver 18 for SQL Server};'
            r'SERVER=DESKTOP-MPVS60R\MSSQLSERVER01;'  # Replace with your desktop server details
            r'DATABASE=ChargeMaster_Users;'
            r'Trusted_Connection=yes;'
            r'TrustServerCertificate=yes;'
        )

    return pyodbc.connect(conn_str)

def test_db_connection():
    try:
        conn = get_connection_UsersDB()
        print("Successfully connected to the database.")
        # You can perform a simple query to test the connection further
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        row = cursor.fetchone()
        print("Database version:", row[0])
    except pyodbc.Error as e:
        print("Database connection failed:", e)
    finally:
        if conn:
            conn.close()


def create_user_charge_sheet(user_id):
    conn = get_connection_UsersDB()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO UserChargeSheet (UserID) VALUES (?)", user_id)
    conn.commit()
    cursor.execute("SELECT @@IDENTITY AS ID")
    user_charge_sheet_id = cursor.fetchone()[0]
    conn.close()
    return user_charge_sheet_id


def get_chargesheet_by_user_ID(user_ID):
    conn = get_connection_UsersDB()
    try:
        with conn.cursor() as cursor:
            # SQL query to fetch chargesheet details for a given user ID
            query = "SELECT * FROM UserChargeSheet WHERE UserID = ?"
            cursor.execute(query, (user_ID,))
            charge_sheets = [row for row in cursor.fetchall()]
            return charge_sheets
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()



def add_charge_to_sheet(user_charge_sheet_id, user_id, location_id, system_id, charge_id):
    conn = get_connection_UsersDB()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO ChargeSheetDetails (UserChargeSheetID, UserID, LocationID, SystemID, ChargeID) VALUES (?, ?, ?, ?, ?)",
            user_charge_sheet_id, user_id, location_id, system_id, charge_id
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def add_charges_to_sheet(user_charge_sheet_id, user_id, charges):
    conn = get_connection_UsersDB()
    cursor = conn.cursor()
    try:
        for charge in charges:
            location_id = charge['location_id']
            system_id = charge['system_id']
            charge_id = charge['charge_id']
            cursor.execute(
                "INSERT INTO ChargeSheetDetails (UserChargeSheetID, UserID, LocationID, SystemID, ChargeID) VALUES (?, ?, ?, ?, ?)",
                user_charge_sheet_id, user_id, location_id, system_id, charge_id
            )
        conn.commit()
    except Exception as e:
        conn.rollback()  # Rollback in case of error
        raise e
    finally:
        cursor.close()
        conn.close()


def get_charge_details_for_user_chargesheet(user_id, charge_sheet_id):
    conn = get_connection_UsersDB()
    try:
        with conn.cursor() as cursor:
            query = """
            SELECT * FROM ChargeSheetDetails 
            WHERE UserChargeSheetID = ? AND UserID = ?
            """
            cursor.execute(query, (charge_sheet_id, user_id))
            columns = [column[0] for column in cursor.description]
            details = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return details
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()



def update_chargesheet_DB_by_user(updated_chargesheet):
    conn = get_connection_UsersDB()  # Connect to your database
    cursor = conn.cursor()

    try:
        # Assuming the updated_chargesheet object has the necessary attributes
        update_query = """
        UPDATE UserChargeSheet
        SET ChargeSheetName = ?
        WHERE ChargeSheetID = ? AND UserID = ?
        """

        cursor.execute(update_query, (updated_chargesheet.chargesheet_name, updated_chargesheet.chargesheet_id, updated_chargesheet.user_id))
        conn.commit()  # Commit the transaction

        return updated_chargesheet.chargesheet_id
    except pyodbc.Error as e:
        print("Database error:", e)
        return None
    finally:
        cursor.close()
        conn.close()


def is_user_authorized_to_access(chargesheet_id, user_id):
    conn = get_connection_UsersDB()
    try:
        with conn.cursor() as cursor:
            # SQL query to check if the user is the owner of the chargesheet
            query = """
            SELECT COUNT(*) FROM UserChargeSheet
            WHERE UserChargeSheetID = ? AND UserID = ?
            """
            cursor.execute(query, (chargesheet_id, user_id))
            result = cursor.fetchone()
            print(user_id, chargesheet_id, result)
            return result[0] > 0
    except Exception as e:
        print(f"Error checking authorization: {e}")
        return False
    finally:
        conn.close()
        
def is_user_authorized_to_delete(chargesheet_id, user_id):
    conn = get_connection_UsersDB()
    try:
        with conn.cursor() as cursor:
            # SQL query to check if the user is the owner of the chargesheet
            query = """
            SELECT COUNT(*) FROM ChargeMaster_Users.UserChargeSheet
            WHERE UserChargeSheetID = ? AND UserID = ?
            """
            cursor.execute(query, (chargesheet_id, user_id))
            result = cursor.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Error checking authorization: {e}")
        return False
    finally:
        conn.close()



def delete_chargesheet_from_db(chargesheet_id):
    conn = get_connection_UsersDB()
    try:
        with conn.cursor() as cursor:
            # SQL query to delete a chargesheet
            query = "DELETE FROM ChargeMaster_Users.UserChargeSheet WHERE UserChargeSheetID = ?"
            cursor.execute(query, (chargesheet_id,))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error deleting chargesheet: {e}")
        return False
    finally:
        conn.close()



def get_chargesheet_by_id(chargesheet_id):
    conn = get_connection_UsersDB()  # Assuming you have a function to get the database connection
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM ChargeMaster_Users.UserChargeSheet WHERE ChargeSheetID = ?"
            cursor.execute(query, (chargesheet_id,))
            row = cursor.fetchone()
            if row:
                # Convert the row to a dictionary or a similar structure that can be serialized to JSON
                chargesheet = {
                    'ChargeSheetID': row.ChargeSheetID,
                    'UserID': row.UserID,
                    # Add other relevant fields
                }
                return chargesheet
            else:
                return None
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        # Handle the error as needed
    finally:
        conn.close()
        
        
        
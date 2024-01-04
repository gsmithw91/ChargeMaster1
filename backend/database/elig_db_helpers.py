import pyodbc
import os 





def get_connection():
    # Check the environment variable
    app_env = os.getenv('APP_ENV', 'desktop')  # Defaults to 'desktop' if not set
    app_env = 'server'
    if app_env == 'server':
        # Connection string for the server
        conn_str = (
            r"DRIVER={ODBC Driver 18 for SQL Server};" +
            r"SERVER=172.234.28.216;" +  # Replace with your Linode server IP or hostname
            r"DATABASE=ChargeMasterDB;" +
            r"UID=SA;" +            # Replace with your SQL username
            r"PWD=B90b909021!;" +   # Replace with your SQL password
            r"TrustServerCertificate=yes;"  # This might be optional depending on your setup
        )
    else:
        # Connection string for the desktop
        conn_str = (
            r'DRIVER={ODBC Driver 18 for SQL Server};'
            r'SERVER=DESKTOP-MPVS60R\MSSQLSERVER01;'  # Replace with your desktop server details
            r'DATABASE=ChargeMasterDB;'
            r'Trusted_Connection=yes;'
            r'TrustServerCertificate=yes;'
        )

    return pyodbc.connect(conn_str)

elig_system_id_to_table_mapping = {
    1: 'Elig_Advocate',
    2: 'Elig_LoyolaIns',
    3: 'Elig_NorthShore',
    4: 'Elig_Northwestern',
    5: 'Elig_Rush',
    6: 'Elig_UCMC'
}



# New function to get all records from a specific elig table based on system ID
def get_all_elig_records(elig_system_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Get the table name based on the system ID
        table_name = elig_system_id_to_table_mapping.get(elig_system_id)
        if not table_name:
            raise ValueError(f"No table mapping found for system ID: {elig_system_id}")

        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except pyodbc.Error as e:
        print("Database error:", e)
    except ValueError as ve:
        print("Value error:", ve)
    finally:
        if conn:
            conn.close()
            
            
# Function to get records from a specific elig table based on system ID and LocationID
def get_elig_records_by_location(elig_system_id, location_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Get the table name based on the system ID
        table_name = elig_system_id_to_table_mapping.get(elig_system_id)
        if not table_name:
            raise ValueError(f"No table mapping found for system ID: {elig_system_id}")

        query = f"SELECT * FROM {table_name} WHERE LocationID = ?"
        cursor.execute(query, (location_id,))
        rows = cursor.fetchall()
        return rows
    except pyodbc.Error as e:
        print("Database error:", e)
    except ValueError as ve:
        print("Value error:", ve)
    finally:
        if conn:
            conn.close()
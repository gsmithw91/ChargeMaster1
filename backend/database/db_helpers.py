# backend/db_helpers.py
import pyodbc

def get_connection():
    conn_str = (
        r'DRIVER={ODBC Driver 18 for SQL Server};'
        r'SERVER=DESKTOP-MPVS60R\MSSQLSERVER01;'
        r'DATABASE=ChargeMasterDB;'
        r'Trusted_Connection=yes;'
        r'TrustServerCertificate=yes;'
    )
    return pyodbc.connect(conn_str)
def get_table_data(table_name):
    # Assume table_name is safe to use or has been validated/sanitized
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            query = f"SELECT * FROM {table_name}"  # Be certain 'table_name' is not user-controlled or is properly sanitized
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            data = []
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))
            return data
    except pyodbc.Error as e:
        print("Database error:", e)
    finally:
        conn.close()
        
def get_available_locations():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT LocationName FROM HospitalLocation")
            return cursor.fetchall()
    finally:
        conn.close()

def get_locations_by_system_id(system_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM HospitalLocation WHERE SystemID = ?", (system_id,))
            columns = [column[0] for column in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return data
    finally:
        conn.close()

# Define the mapping outside of the function
system_id_to_table_mapping = {
    1: 'Charges_Advocate',
    2: 'Charges_LoyolaIns',
    3: 'Charges_NorthShore',
    4: 'Charges_NorthWestern',
    5: 'Charges_Rush',
    6: 'Charges_UCMC'
}

def get_charge_data_by_system_id(system_id, model):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Use the mapping to get the table name
            table_name = system_id_to_table_mapping.get(system_id)
            if table_name is None:
                print(f"No charge table for system ID: {system_id}")
                return None

            # Query the table using the table name from the mapping
            cursor.execute(f"SELECT * FROM {table_name}")
            columns = [column[0] for column in cursor.description]
            # You might not need to instantiate the model here if the tables have different structures
            # Instead, just return the rows as dictionaries
            charge_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return charge_data
    finally:
        conn.close()
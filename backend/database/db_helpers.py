# backend/db_helpers.py
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


def get_filtered_data(table_name, system_id=None, location_id=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Resolve the table name using system_id if provided
            if system_id is not None:
                table_name = charges_system_id_to_table_mapping.get(system_id, table_name)

            base_query = f"SELECT * FROM {table_name}"
            conditions = []
            params = []
            
            if system_id is not None:
                conditions.append("SystemID = ?")
                params.append(system_id)
            
            if location_id is not None:
                conditions.append("LocationID = ?")
                params.append(location_id)
            
            if conditions:
                query = f"{base_query} WHERE {' AND '.join(conditions)}"
            else:
                query = base_query
            
            cursor.execute(query, params)
            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return results
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()




def get_system_by_id(system_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM HospitalSystem WHERE SystemID = ?", (system_id,))
            columns = [column[0] for column in cursor.description]
            row = cursor.fetchone()  # Fetch the first row since SystemID should be unique
            if row:
                return dict(zip(columns, row))
            return None
    finally:
        conn.close()


def get_all_locations():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM HospitalLocation")
            columns = [column[0] for column in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return data
    finally:
        conn.close()



def get_available_location_names():
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




def get_location_details(location_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM HospitalLocation WHERE LocationID = ?", (location_id,))
            columns = [column[0] for column in cursor.description]
            results = cursor.fetchone()  # Assuming LocationID is unique and only one record is returned
            if results:
                return dict(zip(columns, results))
            else:
                return None
    finally:
        conn.close()

# Define the mapping outside of the function
charges_system_id_to_table_mapping = {
    1: 'Charges_Advocate',
    2: 'Charges_LoyolaIns',
    3: 'Charges_NorthShore',
    4: 'Charges_NorthWestern',
    5: 'Charges_Rush',
    6: 'Charges_UCMC'
}

        


def get_insurances_by_system_id(system_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Assuming there is a relationship between systems and insurances
            # and the relevant table and column names are correctly provided
            cursor.execute("SELECT * FROM InsurancePlans WHERE SystemID = ?", (system_id,))
            columns = [column[0] for column in cursor.description]
            insurances = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return insurances
    except pyodbc.Error as e:
        print("Database error:", e)
        return []
    finally:
        conn.close()

elig_system_id_to_table_mapping = {
    1: 'Elig_Advocate',
    2: 'Elig_LoyolaIns',
    3: 'Elig_NorthShore',
    4: 'Elig_NorthWestern',
    5: 'Elig_Rush',
    6: 'Elig_UCMC'
}
def get_in_network_eligibility(system_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            table_name = elig_system_id_to_table_mapping.get(system_id)
            if not table_name:
                return []

            sql = f"SELECT * FROM {table_name} WHERE InNetwork = 1"
            cursor.execute(sql)
            results = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
            return results
    except pyodbc.Error as e:
        return []
    finally:
        conn.close()

        
        


def get_insurance_plan_details(plan_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM InsurancePlans WHERE PlanID = ?", (plan_id,))
            columns = [column[0] for column in cursor.description]
            result = cursor.fetchone()
            if result:
                return dict(zip(columns, result))
            else:
                return None
    finally:
        conn.close()








def get_insurance_plans(system_id=None, location_id=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            base_query = "SELECT * FROM InsurancePlans"
            conditions = []
            params = []
            
            if system_id is not None:
                conditions.append("SystemID = ?")
                params.append(system_id)
            
            if location_id is not None:
                conditions.append("LocationID = ?")
                params.append(location_id)
            
            if conditions:
                query = f"{base_query} WHERE {' AND '.join(conditions)}"
            else:
                query = base_query
            
            cursor.execute(query, params)
            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return results
    finally:
        conn.close()




def get_insurance_types():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM InsuranceTypes")
            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return results
    finally:
        conn.close()


        
def get_charge_data(system_id, location_id=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Use the mapping to get the table name
            table_name = charges_system_id_to_table_mapping.get(system_id)
            if table_name is None:
                print(f"No charge table for system ID: {system_id}")
                return None, None

            query = f"SELECT * FROM {table_name}"
            params = []

            if location_id is not None:
                query += " WHERE LocationID = ?"
                params.append(location_id)

            cursor.execute(query, params)
            columns = [column[0] for column in cursor.description]
            charge_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return charge_data, columns
    finally:
        conn.close()

def get_all_insurance_plans():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM InsurancePlans")
            columns = [column[0] for column in cursor.description]
            plans = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return plans
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()



def get_all_carriers():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Carriers")
            columns = [column[0] for column in cursor.description]
            carriers = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return carriers
    finally:
        conn.close()

def get_carrier_by_id(carrier_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Carriers WHERE CarrierID = ?", (carrier_id,))
            columns = [column[0] for column in cursor.description]
            carrier = cursor.fetchone()
            if carrier:
                return dict(zip(columns, carrier))
            return None
    finally:
        conn.close()


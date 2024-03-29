# backend/db_helpers.py
import pyodbc
import os 


def get_connecetion():
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


def get_column_names_from_table(table_name):
    conn = get_connecetion()
    try:
        with conn.cursor() as cursor:
            # Execute a query to fetch the column names from the specified table
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = ?", (table_name,))
            column_names = [row[0] for row in cursor.fetchall()]
            return column_names
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()




def get_filtered_data(table_name, system_id=None, location_id=None):
    conn = get_connecetion()
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
    conn = get_connecetion()
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
    conn = get_connecetion()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM HospitalLocation")
            columns = [column[0] for column in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return data
    finally:
        conn.close()



def get_available_location_names():
    conn = get_connecetion()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT LocationName FROM HospitalLocation")
            return cursor.fetchall()
    finally:
        conn.close()


def get_locations_by_system_id(system_id):
    conn = get_connecetion()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM HospitalLocation WHERE SystemID = ?", (system_id,))
            columns = [column[0] for column in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return data
    finally:
        conn.close()



def get_location_details(location_id):
    conn = get_connecetion()
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

def get_all_insurance_plans():
    conn = get_connecetion()
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

def get_insurance_by_plan_id(plan_id):
    conn = get_connecetion()
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM InsurancePlans WHERE PlanID = ?"
            cursor.execute(query, (plan_id,))
            columns = [column[0] for column in cursor.description]
            result = cursor.fetchone()
            if result:
                return dict(zip(columns, result))
            else:
                return None
    finally:
        conn.close()



def get_insurance_plans(system_id=None, location_id=None):
    conn = get_connecetion()
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



def get_insurance_plan_details(plan_id):
    conn = get_connecetion()
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


def get_insurance_types():
    conn = get_connecetion()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM InsuranceTypes")
            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return results
    finally:
        conn.close()

def get_insurance_type_by_id(insurance_type_id):
    conn = get_connecetion()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM InsuranceTypes WHERE InsuranceTypeID = ?", (insurance_type_id,))
            columns = [column[0] for column in cursor.description]
            result = cursor.fetchone()
            if result:
                return dict(zip(columns, result))
            return None
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
    conn = get_connecetion()
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


def get_all_carriers():
    conn = get_connecetion()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Carriers")
            columns = [column[0] for column in cursor.description]
            carriers = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return carriers
    finally:
        conn.close()

def get_carrier_by_id(carrier_id):
    conn = get_connecetion()
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

charges_system_id_to_table_mapping = {
    1: 'Charges_Advocate',
    2: 'Charges_LoyolaIns',
    3: 'Charges_NorthShore',
    4: 'Charges_NorthWestern',
    5: 'Charges_Rush',
    6: 'Charges_UCMC'
}
        
def get_charge_data(system_id, location_id=None, filter_value=None, filter_type='ServiceDescription'):
    conn = get_connecetion()
    try:
        with conn.cursor() as cursor:
            # Use the mapping to get the table name
            table_name = charges_system_id_to_table_mapping.get(system_id)
            if table_name is None:
                print(f"No charge table for system ID: {system_id}")
                return None, None

            query = f"SELECT * FROM {table_name}"
            params = []
            conditions = []

            if location_id is not None:
                conditions.append("LocationID = ?")
                params.append(location_id)

            if filter_value is not None:
                if filter_type == 'ServiceDescription':
                    conditions.append("ServiceDescription LIKE ?")
                elif filter_type == 'BillingCode':
                    conditions.append("BillingCode LIKE ?")
                else:
                    raise ValueError("Invalid filter type. Must be 'ServiceDescription' or 'BillingCode'.")
                params.append(f"%{filter_value}%")

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            cursor.execute(query, params)
            columns = [column[0] for column in cursor.description]
            charge_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return charge_data, columns
    finally:
        conn.close()


def get_all_charges_by_description(description_search):
    print(f"Function called: Searching across all tables for description like '{description_search}'")
    conn = get_connecetion()
    all_charges_data = []

    try:
        with conn.cursor() as cursor:
            # Iterate through each table in the mapping
            for system_id, table_name in charges_system_id_to_table_mapping.items():
                print(f"Querying table: {table_name}")
                # Construct the SQL query for each table
                query = f"SELECT *, '{system_id}' as SystemID FROM {table_name} WHERE ServiceDescription LIKE ?"
                params = [f"%{description_search}%"]

                # Execute the query
                cursor.execute(query, params)
                # Fetch the results
                charge_data = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
                # Append the results from this table to the overall list
                all_charges_data.extend(charge_data)
                print(f"Records found in {table_name}: {len(charge_data)}")

    except pyodbc.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"General error in get_all_charges_by_description: {e}")

    finally:
        conn.close()

    return all_charges_data



def get_all_charges_by_billing_code(filter_value):
    print(f"Function called: Searching across all tables for billing code like '{filter_value}'")
    conn = get_connecetion()
    all_charges_data = []

    try:
        with conn.cursor() as cursor:
            # Iterate through each table in the mapping
            for system_id, table_name in charges_system_id_to_table_mapping.items():
                print(f"Querying table: {table_name}")
                # Construct the SQL query for each table
                query = f"SELECT *, '{system_id}' as SystemID FROM {table_name} WHERE BillingCode LIKE ?"
                params = [f"%{filter_value}%"]

                # Execute the query
                cursor.execute(query, params)
                # Fetch the results
                charge_data = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
                # Append the results from this table to the overall list
                all_charges_data.extend(charge_data)
                print(f"Records found in {table_name}: {len(charge_data)}")

    except pyodbc.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"General error in get_all_charges_by_billing_code: {e}")

    finally:
        conn.close()

    return all_charges_data



def get_insurance_plans_by_carrier_id(carrier_id):
    conn = get_connecetion()
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM InsurancePlans WHERE CarrierID = ?"
            cursor.execute(query, (carrier_id,))
            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return results
    finally:
        conn.close()
        


def get_insurance_info_by_carrier(carrier_id):
    conn = get_connecetion()
    try:
        with conn.cursor() as cursor:
            query = """
            SELECT 
                Carriers.*, 
                InsurancePlans.*, 
                InsuranceTypes.*
            FROM 
                Carriers
            JOIN 
                InsurancePlans ON Carriers.CarrierID = InsurancePlans.CarrierID
            JOIN 
                InsuranceTypes ON InsurancePlans.InsuranceTypeID = InsuranceTypes.InsuranceTypeID
            WHERE 
                Carriers.CarrierID = ?
            """
            cursor.execute(query, (carrier_id,))
            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return results
    finally:
        conn.close()

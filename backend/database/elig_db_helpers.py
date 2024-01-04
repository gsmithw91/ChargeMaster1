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


def get_all_elig_records(system_id, location_id=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Get the table name based on the system ID
            table_name = elig_system_id_to_table_mapping.get(system_id)
            if not table_name:
                raise ValueError(f"No table mapping found for system ID: {system_id}")

            # Prepare and execute the query
            if location_id is not None:
                query = f"SELECT * FROM {table_name} WHERE LocationID = ?"
                cursor.execute(query, (location_id,))
            else:
                query = f"SELECT * FROM {table_name}"
                cursor.execute(query)

            # Fetch and structure the data
            columns = [column[0] for column in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return data
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return None
    except ValueError as ve:
        print(f"Value error: {ve}")
        return None
    finally:
        conn.close()

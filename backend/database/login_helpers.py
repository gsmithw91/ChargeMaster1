import pyodbc
import os
from flask_bcrypt import Bcrypt

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

# Initialize Bcrypt
bcrypt = Bcrypt()

# Function to hash a password
def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

# Function to check a hashed password
def check_password(hashed_password, password):
    return bcrypt.check_password_hash(hashed_password, password)

# Function to register a new user
def register_user(first_name, last_name, email, phone_number, company, user_type_id, password):
    hashed_pwd = hash_password(password)
    conn = get_connection_UsersDB()
    cursor = conn.cursor()
    insert_query = '''
    INSERT INTO STSUsers (UserFirstName, UserLastName, UserEmail, UserPhoneNumber, UserCompany, UserTypeID, UserPassword)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    '''
    try:
        cursor.execute(insert_query, (first_name, last_name, email, phone_number, company, user_type_id, hashed_pwd))
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to authenticate a user
def authenticate_user(email, password):
    conn = get_connection_UsersDB()
    cursor = conn.cursor()
    select_query = 'SELECT UserId, UserPassword FROM STSUsers WHERE UserEmail = ? and IsAuthGS <> 0;'
    try:
        cursor.execute(select_query, (email,))
        user_record = cursor.fetchone()
        if user_record and check_password(user_record[1], password):
            return user_record[0]  # Return the UserId if authentication is successful
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def get_user_info(user_id):
    conn = get_connection_UsersDB()
    cursor = conn.cursor()
    query = '''
    SELECT UserId, UserFirstName, UserLastName, UserEmail, UserPhoneNumber, UserCompany, UserTypeID
    FROM STSUsers
    WHERE UserId = ?;
    '''
    try:
        cursor.execute(query, (user_id,))
        user_info = cursor.fetchone()
        return user_info  # This will be a tuple with user data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
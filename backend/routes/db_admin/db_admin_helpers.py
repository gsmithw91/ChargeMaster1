# backend/db_helpers.py
import pyodbc
import os 
from flask import Blueprint, jsonify, request , url_for, session
from logs.custom_logger import api_logger
import pandas as pd
from pydantic import ValidationError 


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

def get_table_names():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
    table_names = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return table_names


def get_column_names(table_name):
    conn = get_connection()
    cursor = conn.cursor()

    # Updated query with table aliases to avoid ambiguity
    query = f"""
    SELECT 
        cols.COLUMN_NAME, 
        cols.DATA_TYPE, 
        cols.IS_NULLABLE,
        cols.COLUMN_DEFAULT,
        tc.CONSTRAINT_TYPE
    FROM 
        INFORMATION_SCHEMA.COLUMNS AS cols
        LEFT JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS ccu ON cols.TABLE_NAME = ccu.TABLE_NAME AND cols.COLUMN_NAME = ccu.COLUMN_NAME
        LEFT JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc ON ccu.CONSTRAINT_NAME = tc.CONSTRAINT_NAME AND tc.TABLE_NAME = cols.TABLE_NAME
    WHERE 
        cols.TABLE_NAME = N'{table_name}';
    """
    
    cursor.execute(query)
    columns_info = [{
        'column_name': row[0], 
        'data_type': row[1], 
        'is_nullable': row[2],
        'default_value': row[3],
        'constraint_type': row[4]
    } for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    return columns_info

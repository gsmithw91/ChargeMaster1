# backend/db_helpers.py
import pyodbc
import os 
from flask import Blueprint, jsonify, request , url_for, session
from logs.custom_logger import api_logger
import pandas as pd
from pydantic import ValidationError 
from .db_admin_helpers import get_table_names, get_column_names
from logs.custom_logger import api_logger


db_admin_api = Blueprint('db_admin', __name__, url_prefix='/db_admin')

@db_admin_api.route('/tables', methods=['GET'])
def list_tables():
    try:
        tables = get_table_names()
        return jsonify({'tables': tables}), 200
    except Exception as e:
        api_logger.error(f"Error fetching table names: {e}")  # Log the error
        return jsonify({'error': str(e)}), 500
    
    
@db_admin_api.route('/columns/<string:table_name>', methods=['GET'])
def list_columns(table_name):
    try:
        columns_info = get_column_names(table_name)
        return jsonify({'columns_info': columns_info}), 200
    except Exception as e:
        api_logger.error(f"Error fetching column details for table {table_name}: {e}")  # Log the error
        return jsonify({'error': str(e)}), 500

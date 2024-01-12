from flask import Blueprint, render_template, request, json, session, jsonify, send_from_directory, redirect
from backend.database.db_helpers import get_filtered_data
from backend.models.HospitalSystem import HospitalSystem
from backend.models.HospitalLocation import HospitalLocation
from logging.handlers import TimedRotatingFileHandler
import os
from logs.custom_logger import web_logger

web = Blueprint('web', __name__)

# Serve the React app's main entry point
@web.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Serve static files (CSS, JS, images, etc.)
@web.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Redirect all non-API requests to the index.html for React Router to handle
@web.route('/<path:path>', methods=['GET'])
def catch_all(path):
    return send_from_directory('static', 'index.html')
from flask import Blueprint, render_template, request, json, session, jsonify, send_from_directory, redirect
from backend.database.db_helpers import get_filtered_data
from backend.models.HospitalSystem import HospitalSystem
from backend.models.HospitalLocation import HospitalLocation
import logging
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
    if filename.endswith(".glb"):
        return send_from_directory('static', filename, mimetype='application/octet-stream')
    else:
        return send_from_directory('static', filename)

# Route for serving the privacy policy from the static directory
@web.route('/privacy-policy')
def privacy_policy():
    return send_from_directory('static', 'privacy.html')
# # Redirect all non-API requests to the index.html for React Router to handle
# @web.route('/<path:path>', methods=['GET'])
# def catch_all(path):
#     return send_from_directory('static', 'index.html')


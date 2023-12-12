# backend/routes/error_routes.py
from flask import Blueprint, jsonify
from logs.custom_logger import error_logger

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
    error_logger.error(f"404 error: {error}")  # Log the error
    return jsonify({'error': 'Resource not found'}), 404

@errors.app_errorhandler(500)
def error_500(error):
    error_logger.error(f"500 error: {error}")  # Log the error
    return jsonify({'error': 'An internal error occurred'}), 500

# You can add more error handlers for different error codes as needed

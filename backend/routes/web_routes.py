# backend/routes/web_routes.py
from flask import Blueprint, render_template, request
from backend.database.db_helpers import get_filtered_data
from backend.models.HospitalSystem import HospitalSystem
from backend.models.HospitalLocation import HospitalLocation
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from logs.custom_logger import web_logger

web = Blueprint('web', __name__)


@web.route('/')
def index():
    return render_template('index.html')


@web.route('/chargemaster')
def chargemaster():
    web_logger.info(f"Accessed the home page with method {request.method} and headers {request.headers}")
    try:
        # Use the updated get_filtered_data function without system_id and location_id
        systems_data = get_filtered_data("HospitalSystem")
        systems = [HospitalSystem(**system).dict() for system in systems_data]
        return render_template('chargemaster.html', systems=systems)
    except ValidationError as e:
        web_logger.error(f"Data validation error for systems: {e}")
        # Handle the error as you see fit (e.g., show a custom error page)
        return render_template('error.html', error="Invalid data format"), 500
    except Exception as e:
        web_logger.error(f"An error occurred while accessing the home page: {e}")
        # Handle the error as you see fit (e.g., show a custom error page)
        return render_template('error.html', error="An error occurred"), 500


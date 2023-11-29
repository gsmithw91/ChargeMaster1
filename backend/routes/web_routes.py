# backend/routes/web_routes.py
from flask import Blueprint, render_template, request
from backend.database.db_helpers import get_table_data
from backend.models.HospitalSystem import HospitalSystem
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from logs.custom_logger import get_web_logger

web = Blueprint('web', __name__)

web_logger = get_web_logger()


@web.route('/')
def index():
    web_logger.info(f"Accessed the home page with method {request.method} and headers {request.headers}")
    systems_data = get_table_data("HospitalInfo", "HospitalSystem")
    systems = [HospitalSystem(**system).dict() for system in systems_data]
    return render_template('index.html', systems=systems)
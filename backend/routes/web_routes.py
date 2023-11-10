# backend/routes/web_routes.py
from flask import Blueprint, render_template
from backend.database.db_helpers import get_table_data
from backend.models.HospitalSystem import HospitalSystem

web = Blueprint('web', __name__)

@web.route('/')
def index():
    systems_data = get_table_data("HospitalSystem")
    systems = [HospitalSystem(**system).dict() for system in systems_data]
    return render_template('index.html', systems=systems)

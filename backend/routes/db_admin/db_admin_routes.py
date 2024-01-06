from pydantic import ValidationError 
from flask import Blueprint, jsonify, request , url_for, session
from logs.custom_logger import api_logger
import pandas as pd
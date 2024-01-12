# backend/routes/login/login_routes.py
from flask import Blueprint, jsonify, request
from backend.database.login_helpers import register_user, authenticate_user

login_api = Blueprint('login_api', __name__, url_prefix='/auth')

@login_api.route('/register', methods=['POST'])
def user_register():
    try:
        data = request.json
        register_user(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone_number=data['phone_number'],
            company=data['company'],
            user_type_id=data['user_type_id'],
            password=data['password']
        )
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@login_api.route('/authenticate', methods=['POST'])
def user_authenticate():
    try:
        data = request.json
        user_id = authenticate_user(
            email=data['email'],
            password=data['password']
        )
        if user_id:
            return jsonify({'message': 'User authenticated successfully', 'user_id': user_id}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# backend/routes/login/login_routes.py
from flask import Blueprint, jsonify, request
from backend.database.login_helpers import register_user, authenticate_user, get_user_info
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import traceback

login_api = Blueprint('login_api', __name__, url_prefix='/auth')

# Configure Flask-JWT-Extended
jwt = JWTManager()

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
            # Create a JWT token with the user's ID
            access_token = create_access_token(identity=user_id)
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@login_api.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_info_route(user_id):
    try:
        current_user_id = get_jwt_identity()
        if user_id != current_user_id:
            return jsonify({'message': 'Unauthorized'}), 403

        user_data = get_user_info(user_id)
        if user_data:
            response = {
                "UserId": user_data[0],
                "FirstName": user_data[1],
                "LastName": user_data[2],
                "Email": user_data[3],
                "PhoneNumber": user_data[4],
                "Company": user_data[5],
                "UserTypeID": user_data[6],
            }
            return jsonify(response), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

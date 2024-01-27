from flask import Flask, jsonify, send_from_directory   
from flask_cors import CORS  # Import the CORS module
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from backend.routes.chargemaster.charges_api_routes import api
from backend.routes.chargemaster.charges_error_routes import errors
from backend.routes.chargemaster.charges_web_routes import web
from backend.routes.chargemaster.charges_react_api_routes import react_api
from backend.routes.eligbilitytool.elig_react_api_routes import elig_api
from backend.routes.db_admin.db_admin_routes import db_admin_api
from backend.routes.login.login_routes import login_api  
from backend.routes.chargesheet.chargesheet_routes import chargesheet_api


app = Flask(__name__, static_url_path='/static')
app.secret_key = 'fappie'

app.config['JWT_SECRET_KEY'] = 'STS91GS'  # Replace with your own secret key
jwt = JWTManager(app)


# Enable CORS for your app
CORS(app, origins="http://localhost:3000, https://smithtech.io", supports_credentials=True)





# Register the blueprints
app.register_blueprint(api)
app.register_blueprint(errors)
app.register_blueprint(web)
app.register_blueprint(react_api)
app.register_blueprint(elig_api)
app.register_blueprint(db_admin_api)
app.register_blueprint(login_api)  
app.register_blueprint(chargesheet_api)  

@app.route('/json-file', methods=['GET'])
def get_json_file():
    try:
        # Return the JSON file from the static folder
        return app.send_static_file('smithtech_openapi_with_insights.json')
    except Exception as e:
        return jsonify({"error": "An error occurred while serving the JSON file"}), 500





if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

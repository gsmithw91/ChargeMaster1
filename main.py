# main.py
from flask import Flask, jsonify
from flask_cors import CORS  # Import the CORS module
from backend.routes.chargemaster.charges_api_routes import api
from backend.routes.chargemaster.charges_error_routes import errors
from backend.routes.chargemaster.charges_web_routes import web
from backend.routes.chargemaster.charges_react_api_routes import react_api
from backend.routes.eligbilitytool.elig_react_api_routes import elig_api
from backend.routes.db_admin.db_admin_routes import db_admin_api

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'fappie'

# Enable CORS for your app
CORS(app, resources={r"/react/*": {"origins": "http://localhost:3000"}})  # Replace with the appropriate route

# Register the blueprint
app.register_blueprint(api)
app.register_blueprint(errors)
app.register_blueprint(web)
app.register_blueprint(react_api)
app.register_blueprint(elig_api)
app.register_blueprint(db_admin_api)


@app.route('/json-file', methods=['GET'])
def get_json_file():
    try:
        # Return the JSON file from the static folder
        return app.send_static_file('smithtech_openapi_with_insights.json')
    except Exception as e:
        return jsonify({"error": "An error occurred while serving the JSON file"}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

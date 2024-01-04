# main.py
from flask import Flask
from flask_cors import CORS  # Import the CORS module
from backend.routes.chargemaster.charges_api_routes import api
from backend.routes.chargemaster.charges_error_routes import errors
from backend.routes.chargemaster.charges_web_routes import web
from backend.routes.chargemaster.charges_react_api_routes import react_api
from backend.routes.eligbilitytool.elig_react_api_routes import elig_api


app = Flask(__name__)
app.secret_key = 'fappie'

# Enable CORS for your app
CORS(app, resources={r"/react/*": {"origins": "http://localhost:3000"}})  # Replace with the appropriate route

# Register the blueprint
app.register_blueprint(api)
app.register_blueprint(errors)
app.register_blueprint(web)
app.register_blueprint(react_api)
app.register_blueprint(elig_api)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

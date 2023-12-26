# main.py
from flask import Flask
from flask_cors import CORS
from backend.routes.chargemaster.charges_api_routes import api
from backend.routes.chargemaster.charges_error_routes import errors
from backend.routes.chargemaster.charges_web_routes import web
from backend.routes.chargemaster.charges_react_api_routes import react_api



app = Flask(__name__)
app.secret_key = 'fappie'
CORS(app)

# Register the blueprint
app.register_blueprint(api)
app.register_blueprint(errors)
app.register_blueprint(web)
app.register_blueprint(react_api)
#from . import app

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
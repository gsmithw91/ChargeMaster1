# main.py
from flask import Flask
from backend.routes.api_routes import api
from backend.routes.error_routes import errors
from backend.routes.web_routes import web


app = Flask(__name__)

# Register the blueprint
app.register_blueprint(api)
app.register_blueprint(errors)
app.register_blueprint(web)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)  # Run on localhost and port 5000

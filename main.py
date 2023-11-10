# main.py
from flask import Flask
from backend.routes.api_routes import api

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(api)

if __name__ == '__main__':
    app.run(debug=True)

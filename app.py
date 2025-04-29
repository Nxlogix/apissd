from flask import Flask, redirect, url_for
from flasgger import Swagger
from config import db, migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS  
from flask_jwt_extended import JWTManager

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# JWT
app.config['JWT_SECRET_KEY'] = 'nxlogixssd'
JWTManager(app)

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate.init_app(app, db)

# Swagger setup
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API Usuarios y Productos",
        "description": "Documentación generada automáticamente con Flasgger",
        "version": "1.0.0"
    },
    "basePath": "/api",
    "schemes": ["http", "https"],
    "definitions": {
        "User": {
            "type": "object",
            "properties": {
                "id":   {"type": "integer"},
                "name": {"type": "string"},
                "email":{"type": "string"}
            }
        },
        "Product": {
            "type": "object",
            "properties": {
                "id":          {"type": "integer"},
                "name":        {"type": "string"},
                "price":       {"type": "number"},
                "stock":       {"type": "integer"},
                "category_id": {"type": "integer"}
            }
        },
        "Category": {
            "type": "object",
            "properties": {
                "id":          {"type": "integer"},
                "name":        {"type": "string"},
                "description": {"type": "string"}
            }
        }
    }
}
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
Swagger(app, template=swagger_template, config=swagger_config)

# Redirección a Swagger UI al acceder a la raíz
@app.route('/')
def index():
    return redirect(url_for('flasgger.apidocs'))

# Register routes
from routes.user import app_bp
app.register_blueprint(app_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)

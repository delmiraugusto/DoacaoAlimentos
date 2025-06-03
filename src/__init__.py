from flask import Flask
from flask_restful import Api
from src.routes.endpoints import initialize_endpoints
from src.models.Base import db
from flask_jwt_extended import JWTManager
from flask import jsonify
from sqlalchemy import text


def create_app() -> Flask:

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:123456@localhost:3306/doacaoAlimentos'
    app.config['JWT_SECRET_KEY'] = '12345678'

    db.init_app(app)
    jwt = JWTManager(app)

    # Comando para ativar a venv
    # .\venv\Scripts\Activate.ps1

    # Comando para rodar o programa
    # flask --app manage run --host=0.0.0.0 --port=8080
    
    api = Api(app, prefix="/doacoes")
    initialize_endpoints(api)

    return app
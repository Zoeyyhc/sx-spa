from flask import Flask, Blueprint
from dotenv import load_dotenv
from .log import config_log 
import os
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from flask_restx import Api
from flask_jwt_extended import JWTManager
from app.campus.controller import api as campus_api
from app.user.controller import auth_api
from app.user.__init__ import register_user_lookup
from app.core.converter import CustomEncoder



load_dotenv("./.env")

api_bp = Blueprint("api", os.getenv("FLASK_APP_NAME"), url_prefix="/api/v1")
api = Api(api_bp)
api.add_namespace(campus_api)
api.add_namespace(auth_api)

def create_app():
    app = Flask(os.getenv("FLASK_APP_NAME"))
    app.config.from_prefixed_env()
    app.config["JWT_TOKEN_LOCATION"] = ["headers","cookies"]
    app.json_encoder = CustomEncoder
    app.config["RESTX_JSON"]={"cls":CustomEncoder}
    print(app.config)

    config_log(app)

    MongoEngine(app)

    jwt: JWTManager = JWTManager(app)
    register_user_lookup(jwt)

    CORS(app)

    app.register_blueprint(api_bp)


    return app
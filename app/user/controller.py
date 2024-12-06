from flask_restx import Namespace, Resource
from flask import request,jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, current_user
from .model import User, get_hashed_password, check_password
import datetime
from .schema import UserSchema

auth_api: Namespace = Namespace("auth")

@auth_api.route("/")
class UserAuthInfo(Resource):
    @jwt_required()
    def get(self):
        return UserSchema.model_validate(current_user)

@auth_api.route("/login")
class Login(Resource):
    def post(self):
        username = request.json.get("username")
        password = request.json.get("password")
        if not username or not password:
            return {"msg":"username or password is empty"},400
        
        user = User.objects(username=username).first()
        if not user:
            return {"msg": "user not found"}, 404
        
        if not check_password(password,user.password):
            return {"msg":"username or password is wrong"},401
        
        jwt_token = create_access_token(identity=str(user.id),expires_delta=datetime.timedelta(days=30))
        response = jsonify({"access_token":jwt_token})   
        set_access_cookies(response,jwt_token)

        return response
        
        

        

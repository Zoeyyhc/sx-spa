from flask_restx import Namespace, Resource
from flask import request,jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, current_user
from .model import User, check_password, Student, Admin, Teacher
import datetime
from .schema import UserSchema, UserListSchema, StudentSchema, StudentCreateSchema, AdminCreateSchema, AdminSchema, TeacherCreateSchema, TeacherSchema,\
    AdminListSchema, StudentListSchema, TeacherListSchema, UserPutSchema    
from app.user.service import unauthorized_user_service, user_service
from app.user import permission_required
from app.campus.model import Campus
from app.exceptions.database_exceptions import DuplicateRecord
from flask_pydantic import validate 

auth_api: Namespace = Namespace("auth")
@auth_api.route("/")
class UserAuthInfo(Resource):
    @jwt_required()
    def get(self):
        return current_user.to_dict()
    
@auth_api.route("/login")
class Login(Resource):
    def post(self):
        username = request.json.get("username")
        password = request.json.get("password")
        if not username or not password:
            return {"message": "username or password is missing"}, 400

        user_list = User.objects(username=username)
        if len(user_list) == 0:
            return {"code": 401, "message": "Username or Password is incorrect"}, 401
        user = user_list[0]
        if not check_password(password, user.password):
            return {"code": 401, "message": "Username or Password is incorrect"}, 401

        jwt_token = create_access_token(
            identity=str(user.id), expires_delta=datetime.timedelta(days=30)
        )
        response = jsonify({"access_token": jwt_token})
        set_access_cookies(response, jwt_token)
        return response
        

users_api: Namespace = Namespace("users")
@users_api.route("")
class UsersAPi(Resource) :
    @permission_required("users_admin")
    def get(self):
        user_type: str | None = request.args.get("type", None)
        campus: str | None = request.args.get("campus", None)
        if campus is not None:
            campus = Campus.objects(id=campus).first_or_404("Campus not found")

        user_list = user_service().list_users(user_type=user_type, campus=campus)
        if user_type == "admin":
            return AdminListSchema.from_orm(user_list)
        if user_type == "teacher":
            return TeacherListSchema.from_orm(user_list)
        if user_type == "student":
            return StudentListSchema.from_orm(user_list)
        else:
            return UserListSchema.from_orm(user_list)
        
@users_api.route("/<username>")
class UserApi(Resource):
    @jwt_required()
    def get(self, username):
        return UserSchema.from_orm(user_service().get_user(username=username)), 200
    @jwt_required()
    def delete(self, username):
        user_service().delete_user(username=username)
        return
    @jwt_required()
    def put(self, username):
        user_service().update_user(username, **request.json)
        return
    
students_api: Namespace = Namespace("students")
@students_api.route("")
class StudentsApi(Resource):
    def post(self):
        request_data = request.json
        if "campus" not in request_data:
            return {"code": 400, "message": "Campus is not found in the payload"}, 400
        request_data["campus"] = Campus.objects(id=request_data["campus"]).first_or_404(
            "Campus not found"
        )
        student = StudentCreateSchema(**request_data)
        student = Student(**student.dict())
        student = unauthorized_user_service().register_user(student)
        return StudentSchema.from_orm(student), 201


admins_api = Namespace("admins")
@admins_api.route("")
class AdminApi(Resource):
    @permission_required("sys_owner")
    def post(self):
        request_data = request.json
        if "campus" not in request_data:
            return {"code": 400, "message": "Campus is not found in the payload"}, 400
        request_data["campus"] = Campus.objects(id=request_data["campus"]).first_or_404(
            "Campus not found"
        )
        admin = AdminCreateSchema(**request_data)
        admin = Admin(**admin.dict())
        admin = user_service().register_user(admin)
        return AdminSchema.from_orm(admin), 201

teachers_api = Namespace("teachers")


@teachers_api.route("")
class TeacherApi(Resource):
    @permission_required("sys_owner")
    def post(self):
        request_data = request.json
        if "campus" not in request_data:
            return {"code": 400, "message": "Campus is not found in the payload"}, 400
        request_data["campus"] = Campus.objects(id=request_data["campus"]).first_or_404(
            "Campus not found"
        )
        teacher = TeacherCreateSchema(**request_data)
        teacher = Teacher(**teacher.dict())
        teacher = user_service().register_user(teacher)
        return TeacherSchema.from_orm(teacher), 201
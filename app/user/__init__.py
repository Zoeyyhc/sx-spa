from .model import User
from flask_jwt_extended import jwt_required, current_user
import functools
from app.exceptions.permission_exceptions import PermissionDenied

def register_user_lookup(jwt):
    def user_lookup_callback(_jwt_header, jwt_data):
        identifyL = jwt_data["sub"]

        return User.objects(id=identifyL).first_or_404(message="user not found")
    
    jwt.user_lookup_loader(user_lookup_callback)

def permission_required(permission = None):
    def wrapper(func):
        @jwt_required()
        @functools.wraps(func)
        def decorator(*args, **kwargs):  # invoke decorator first then invoke func
            if current_user._cls == "User.Admin":
                if permission is None or permission in current_user.permissions:
                    return func(*args, **kwargs)
                else:
                    raise PermissionDenied(f"Permission '{permission}' is required")    
            raise PermissionDenied     
        return decorator
    return wrapper
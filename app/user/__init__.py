from .model import User

def register_user_lookup(jwt):
    def user_lookup_callback(_jwt_header, jwt_data):
        identifyL = jwt_data["sub"]

        return User.objects(id=identifyL).first_or_404(message="user not found")
    
    jwt.user_lookup_loader(user_lookup_callback)

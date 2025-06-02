from src.controllers.UsersController import UserListResource, UserResource, UserLoginResource

def initialize_endpoints(api):
    api.add_resource(UserListResource, '/usuarios')
    api.add_resource(UserResource, '/usuarios/<int:user_id>')
    api.add_resource(UserLoginResource, '/usuarios/login')

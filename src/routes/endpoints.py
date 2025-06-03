from src.controllers.UsersController import UserListResource, UserResource, UserLoginResource, UserByEmailResource
from src.controllers.AlimentoController import AlimentoListResource, AlimentoResource

def initialize_endpoints(api):
    api.add_resource(UserListResource, '/usuarios')
    api.add_resource(UserResource, '/usuarios/<int:user_id>')
    api.add_resource(UserLoginResource, '/usuarios/login')
    # api.add_resource(UserByEmailResource, '/user/email')


    api.add_resource(AlimentoListResource, '/alimentos')
    api.add_resource(AlimentoResource, '/alimentos/<int:alimento_id>')
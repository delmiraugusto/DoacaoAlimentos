from src.controllers.UsersController import UserListResource, UserResource, UserLoginResource, UserByEmailResource
from src.controllers.AlimentoController import AlimentoListResource, AlimentoResource
from src.controllers.EnderecoController import EnderecoListResource, EnderecoResource

def initialize_endpoints(api):

    # Users
    api.add_resource(UserListResource, '/usuarios')
    api.add_resource(UserResource, '/usuarios/<int:user_id>')
    api.add_resource(UserLoginResource, '/usuarios/login')
    # api.add_resource(UserByEmailResource, '/user/email')

    # Alimento
    api.add_resource(AlimentoListResource, '/alimentos')
    api.add_resource(AlimentoResource, '/alimentos/<int:alimento_id>')

    # Endereco
    api.add_resource(EnderecoListResource, '/enderecos')
    api.add_resource(EnderecoResource, '/enderecos/<int:endereco_id>')

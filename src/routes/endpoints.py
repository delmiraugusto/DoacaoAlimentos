from src.controllers.UsersController import UserListResource, UserResource, UserLoginResource, UserByEmailResource
from src.controllers.AlimentoController import AlimentoListResource, AlimentoResource
from src.controllers.EnderecoController import EnderecoListResource, EnderecoResource
from src.controllers.StatusController import StatusListResource, StatusResource
from src.controllers.PerfilController import PerfilListResource, PerfilResource



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

    # Status
    api.add_resource(StatusListResource, '/status')
    api.add_resource(StatusResource, '/status/<int:status_id>')
    
    # Perfil
    api.add_resource(PerfilListResource, '/perfil')
    api.add_resource(PerfilResource, '/perfil/<int:perfil_id>')
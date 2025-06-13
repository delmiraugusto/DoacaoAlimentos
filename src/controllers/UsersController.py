from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from src.services.UsersService import UserService
from src.models.Base import db
from flask import request
import traceback

user_create_parser = reqparse.RequestParser()
user_create_parser.add_argument('nome', type=str, required=True)
user_create_parser.add_argument('email', type=str, required=True)
user_create_parser.add_argument('senha_hash', type=str, required=True)
user_create_parser.add_argument('telefone', type=str, required=True)
user_create_parser.add_argument('documento', type=str, required=True)
user_create_parser.add_argument('perfil_id', type=str, required=True)
user_create_parser.add_argument('endereco', type=int, required=False)
user_create_parser.add_argument('numero', type=str, required=False)
user_create_parser.add_argument('complemento', type=str, required=False)

user_update_parser = reqparse.RequestParser()
user_update_parser.add_argument('nome', type=str, required=False)
user_update_parser.add_argument('telefone', type=str, required=False)
user_create_parser.add_argument('email', type=str, required=False)
user_update_parser.add_argument('documento', type=str, required=False)
user_update_parser.add_argument('endereco', type=int, required=False)
user_update_parser.add_argument('endereco', type=dict, required=False)
user_update_parser.add_argument('numero', type=str, required=False)
user_update_parser.add_argument('complemento', type=str, required=False)
user_update_parser.add_argument('senha', type=str, required=False)

class UserListResource(Resource):
    #@jwt_required()
    def get(self):
        try:
            user_service = UserService(db.session)
            users = user_service.listar_todos()
            result = []
            for u in users:
                user_dict = {
                    "id": u.id,
                    "nome": u.nome,
                    "email": u.email,
                    "telefone": u.telefone,
                    "documento": u.documento,
                    "perfil_id": u.perfil.nome
                }
                result.append(user_dict)
            return result, 200
        except Exception as e:
            print("Erro ao buscar usuários:", e)
            traceback.print_exc()
            return {"error": str(e)}, 500

    def post(self):
        data = request.get_json()
        user_service = UserService(db.session)
        try:
            user = user_service.criar_usuario(data)
            return {"id": user.id, "msg": "Usuário criado com sucesso"}, 201
        except Exception as e:
            return {"error": str(e)}, 400


class UserResource(Resource):
    # @jwt_required()
    def get(self, user_id):
        user_service = UserService(db.session)
        user = user_service.listar_por_id(user_id)
        if not user:
            return {"msg": "Usuário não encontrado"}, 404
        return {
            "nome": user.nome,
            "email": user.email,
            "telefone": user.telefone,
            "documento": user.documento
        }, 200

    # @jwt_required()
    def put(self, user_id):
        data = request.get_json()
        print("Dados recebidos do request:", data)

        user_service = UserService(db.session)
        try:
            user_service.atualizar_usuario(user_id, data)
            return {"msg": "Usuário atualizado com sucesso"}, 200
        except Exception as e:
            return {"error": str(e)}, 400

    # @jwt_required()
    def delete(self, user_id):
        user_service = UserService(db.session)
        try:
            user_service.deletar_usuario(user_id)
            return {"msg": "Usuário deletado com sucesso"}, 200
        except Exception as e:
            return {"error": str(e)}, 400

class UserByEmailResource(Resource):
    # @jwt_required()
    def get(self):
        email = request.args.get("email")
        if not email:
            return {"msg": "Email é obrigatório"}, 400

        user_service = UserService(db.session)
        try:
            user = user_service.listar_por_email(email)
            if not user:
                return {"msg": "Usuário não encontrado"}, 404
            return {
                "id": user.id,
                "nome": user.nome,
                "email": user.email,
                "telefone": user.telefone,
                "documento": user.documento
            }, 200
        except Exception as e:
            return {"error": str(e)}, 500

class UserLoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, required=True)
        parser.add_argument("senha", type=str, required=True)
        args = parser.parse_args()

        user_service = UserService(db.session)
        user = user_service.autenticar(args["email"], args["senha"])
        if not user:
            return {"msg": "Email ou senha inválidos"}, 401
        
        from flask_jwt_extended import create_access_token
        token = create_access_token(identity=user.id)
        return {"token": token}, 200

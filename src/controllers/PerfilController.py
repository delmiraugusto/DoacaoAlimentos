from flask_restful import Resource, reqparse
from src.services.PerfilService import PerfilService
from src.models.Base import db
from flask import request
import traceback

perfil_create_parser = reqparse.RequestParser()
perfil_create_parser.add_argument('nome', type=str, required=True)

perfil_update_parser = reqparse.RequestParser()
perfil_update_parser.add_argument('nome', type=str, required=False)

class PerfilListResource(Resource):
    #@jwt_required()
    def get(self):
        try:
            perfil_service = PerfilService(db.session)
            perfil = perfil_service.listar_todos()
            result = []
            for u in perfil:
                perfil_dict = {
                    "id": u.id,
                    "nome": u.nome,
                }
                result.append(perfil_dict)
            return result, 200
        except Exception as e:
            print("Erro ao buscar perfis:", e)
            traceback.print_exc()
            return {"error": str(e)}, 500

    def post(self):
        data = request.get_json()
        perfil_service = PerfilService(db.session)
        try:
            perfil = perfil_service.criar_perfil(data)
            return {"id": perfil.id, "msg": "Perfil adicionado com sucesso"}, 201
        except Exception as e:
            return {"error": str(e)}, 400


class PerfilResource(Resource):
    # @jwt_required()
    def get(self, perfil_id):
        try:
            perfil_service = PerfilService(db.session)
            perfil = perfil_service.listar_por_id(perfil_id)
            if not perfil:
                return {"msg": "Perfil não encontrado"}, 404
            return {
                "id": perfil.id,
                "nome": perfil.nome,
            }, 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"error": str(e)}, 500

    # @jwt_required()
    def put(self, perfil_id):
        args = perfil_update_parser.parse_args()
        perfil_service = PerfilService(db.session)
        try:
            perfil = perfil_service.atualizar_perfil(perfil_id, args)
            data = request.get_json()
            print("Dados recebidos do request:", data)
            return {"msg": "Perfil atualizado com sucesso"}, 200
        except Exception as e:
            return {"error": str(e)}, 400

    # @jwt_required()
    def delete(self, perfil_id):
        perfil_service = PerfilService(db.session)
        try:
            perfil_service.deletar_perfil(perfil_id)
            return {"msg": "Perfil deletado com sucesso"}, 200
        except Exception as e:
            return {"error": str(e)}, 400
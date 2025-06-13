from flask_restful import Resource, reqparse
from src.services.StatusService import StatusService
from src.models.Base import db
from flask import request
import traceback

status_create_parser = reqparse.RequestParser()
status_create_parser.add_argument('nome', type=str, required=True)

status_update_parser = reqparse.RequestParser()
status_update_parser.add_argument('nome', type=str, required=False)

class StatusListResource(Resource):
    #@jwt_required()
    def get(self):
        try:
            status_service = StatusService(db.session)
            status = status_service.listar_todos()
            result = []
            for u in status:
                status_dict = {
                    "id": u.id,
                    "nome": u.nome,
                }
                result.append(status_dict)
            return result, 200
        except Exception as e:
            print("Erro ao buscar status:", e)
            traceback.print_exc()
            return {"error": str(e)}, 500

    def post(self):
        data = request.get_json()
        status_service = StatusService(db.session)
        try:
            status = status_service.criar_status(data)
            return {"id": status.id, "msg": "Status adicionado com sucesso"}, 201
        except Exception as e:
            return {"error": str(e)}, 400


class StatusResource(Resource):
    # @jwt_required()
    def get(self, status_id):
        try:
            status_service = StatusService(db.session)
            status = status_service.listar_por_id(status_id)
            if not status:
                return {"msg": "Status não encontrado"}, 404
            return {
                "nome": status.nome,
            }, 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"error": str(e)}, 500

    # @jwt_required()
    def put(self, status_id):
        args = status_update_parser.parse_args()
        status_service = StatusService(db.session)
        try:
            status = status_service.atualizar_status(status_id, args)
            data = request.get_json()
            print("Dados recebidos do request:", data)
            return {"msg": "Status atualizado com sucesso"}, 200
        except Exception as e:
            return {"error": str(e)}, 400

    # @jwt_required()
    def delete(self, status_id):
        status_service = StatusService(db.session)
        try:
            status_service.deletar_status(status_id)
            return {"msg": "Status deletado com sucesso"}, 200
        except Exception as e:
            return {"error": str(e)}, 400
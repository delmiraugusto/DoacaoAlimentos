from flask_restful import Resource, reqparse
from src.services.DoacaoItemService import DoacaoItemService
from src.models.Base import db
from flask import request
import traceback

doacaoItem_create_parser = reqparse.RequestParser()
doacaoItem_create_parser.add_argument('doacao_id', type=str, required=True)
doacaoItem_create_parser.add_argument('alimento_id', type=str, required=False)
doacaoItem_create_parser.add_argument('quantidade', type=str, required=False)
doacaoItem_create_parser.add_argument('data_vencimento', type=str, required=True)

doacaoItem_update_parser = reqparse.RequestParser()
doacaoItem_update_parser.add_argument('doacao_id', type=str, required=False)
doacaoItem_update_parser.add_argument('alimento_id', type=str, required=False)
doacaoItem_update_parser.add_argument('quantidade', type=str, required=False)
doacaoItem_update_parser.add_argument('data_vencimento', type=str, required=False)

class DoacaoItemListResource(Resource):
    #@jwt_required()
    def get(self):
        try:
            doacaoItem_service = DoacaoItemService(db.session)
            doacoesItem = doacaoItem_service.listar_todos()
            result = []
            for d in doacoesItem:
                doacaoItem_dict = {
                    "id": d.id,
                    "doacao_id": d.doacao_id,
                    "alimento_id": d.alimento_id,
                    "quantidade": d.quantidade,
                    "data_vencimento": d.data_vencimento.isoformat() if d.data_vencimento else None,
                }
                result.append(doacaoItem_dict)
            return result, 200
        except Exception as e:
            print("Erro ao buscar doacoesItens:", e)
            traceback.print_exc()
            return {"error": str(e)}, 500

    def post(self):
        data = request.get_json()
        doacaoItem_service = DoacaoItemService(db.session)
        try:
            doacaoItem = doacaoItem_service.criar_doacaoItem(data)
            return {"id": doacaoItem.id, "msg": "DoacaoItem adicionado com sucesso"}, 201
        except Exception as e:
            return {"error": str(e)}, 400
        
class DoacaoItemResource(Resource):
    # @jwt_required()
    def get(self, doacaoItem_id):
        try:
            doacaoItem_service = DoacaoItemService(db.session)
            doacaoItem = doacaoItem_service.listar_por_id(doacaoItem_id)
            if not doacaoItem:
                return {"msg": "DoacaoItem não encontrado"}, 404
            return {
                    "id": doacaoItem.id,
                    "doacao_id": doacaoItem.doacao_id,
                    "alimento_id": doacaoItem.alimento_id,
                    "quantidade": doacaoItem.quantidade,
                    "data_vencimento": doacaoItem.data_vencimento.isoformat() if doacaoItem.data_vencimento else None,
            }, 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"error": str(e)}, 500

    # @jwt_required()
    def put(self, doacaoItem_id):
        args = doacaoItem_update_parser.parse_args()
        doacaoItem_service = DoacaoItemService(db.session)
        try:
            doacaoItem_service.atualizar_doacaoItem(doacaoItem_id, args)
            data = request.get_json()
            print("Dados recebidos do request:", data)
            return {"msg": "DoacaoItem atualizado com sucesso"}, 200
        except Exception as e:
            return {"error": str(e)}, 400

    # @jwt_required()
    def delete(self, doacaoItem_id):
        doacaoItem_service = DoacaoItemService(db.session)
        try:
            doacaoItem_service.deletar_doacaoItem(doacaoItem_id)
            return {"msg": "DoacaoItem deletado com sucesso"}, 200
        except Exception as e:
            return {"error": str(e)}, 400
from flask_restful import Resource, reqparse
from src.services.AlimentoService import AlimentoService
from src.models.Base import db
from flask import request
import traceback

alimento_create_parser = reqparse.RequestParser()
alimento_create_parser.add_argument('nome', type=str, required=True)
alimento_create_parser.add_argument('marca', type=str, required=True)

alimento_update_parser = reqparse.RequestParser()
alimento_update_parser.add_argument('nome', type=str, required=False)
alimento_update_parser.add_argument('marca', type=str, required=False)

class AlimentoListResource(Resource):
    #@jwt_required()
    def get(self):
        try:
            alimento_service = AlimentoService(db.session)
            alimentos = alimento_service.listar_todos()
            result = []
            for u in alimentos:
                alimento_dict = {
                    "id": u.id,
                    "nome": u.nome,
                    "marca": u.marca,
                }
                result.append(alimento_dict)
            return result, 200
        except Exception as e:
            print("Erro ao buscar alimentos:", e)
            traceback.print_exc()
            return {"error": str(e)}, 500

    def post(self):
        data = request.get_json()
        alimento_service = AlimentoService(db.session)
        try:
            alimento = alimento_service.criar_alimento(data)
            return {"id": alimento.id, "msg": "Alimento adicionado com sucesso"}, 201
        except Exception as e:
            return {"error": str(e)}, 400


class AlimentoResource(Resource):
    # @jwt_required()
    def get(self, alimento_id):
        try:
            alimento_service = AlimentoService(db.session)
            alimento = alimento_service.listar_por_id(alimento_id)
            if not alimento:
                return {"msg": "Alimento não encontrado"}, 404
            return {
                "nome": alimento.nome,
                "marca": alimento.marca,
            }, 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"error": str(e)}, 500

    # @jwt_required()
    def put(self, alimento_id):
        args = alimento_update_parser.parse_args()
        alimento_service = AlimentoService(db.session)
        try:
            alimento = alimento_service.atualizar_alimentos(alimento_id, args)
            data = request.get_json()
            print("Dados recebidos do request:", data)
            return {"msg": "Alimento atualizado com sucesso"}, 200
        except Exception as e:
            return {"error": str(e)}, 400

    # @jwt_required()
    def delete(self, alimento_id):
        alimento_service = AlimentoService(db.session)
        try:
            alimento_service.deletar_alimento(alimento_id)
            return {"msg": "Alimento deletado com sucesso"}, 200
        except Exception as e:
            return {"error": str(e)}, 400
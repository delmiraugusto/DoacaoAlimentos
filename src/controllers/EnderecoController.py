from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from src.services.EnderecoService import EnderecoService
from src.models.Base import db
from flask import request
import traceback

endereco_create_parser = reqparse.RequestParser()
endereco_create_parser.add_argument('cep', type=str, required=True)

endereco_update_parser = reqparse.RequestParser()
endereco_update_parser.add_argument('cep', type=str, required=False)

class EnderecoListResource(Resource):
    #@jwt_required()
    def get(self):
        try:
            endereco_service = EnderecoService(db.session)
            enderecos = endereco_service.listar_todos()
            result = []
            for e in enderecos:
                endereco_dict = {
                    "id": e.id,
                    "cep": e.cep,
                    "logradouro": e.logradouro,
                    "bairro": e.bairro,
                    "uf": e.uf,
                    "cidade": e.cidade
                }
                result.append(endereco_dict)
            return result, 200
        except Exception as e:
            print("Erro ao buscar os enderecos:", e)
            traceback.print_exc()
            return {"error": str(e)}, 500

    def post(self):
        data = request.get_json()
        cep = data.get("cep") 

        endereco_service = EnderecoService(db.session)
        try:
            endereco = endereco_service.obter_ou_criar_endereco_por_cep(cep)
            return {"id": endereco.id, "msg": "Endereco criado com sucesso"}, 201
        except Exception as e:
            return {"error": str(e)}, 400


class EnderecoResource(Resource):
    # @jwt_required()
    def get(self, endereco_id):
        endereco_service = EnderecoService(db.session)
        try:
            endereco = endereco_service.listar_por_id(endereco_id)
            return {
                "id": endereco.id,
                "cep": endereco.cep,
                "logradouro": endereco.logradouro,
                "bairro": endereco.bairro,
                "uf": endereco.uf,
                "cidade": endereco.cidade
            }, 200
        except ValueError as e:
            return {"msg": str(e)}, 404

    # @jwt_required()
    def put(self, endereco_id):
        args = endereco_update_parser.parse_args()
        endereco_service = EnderecoService(db.session)
        try:
            endereco = endereco_service.obter_ou_atualizar_endereco(endereco_id, args)
            return {"msg": "Endereco atualizado com sucesso"}, 200
        except Exception as e:
            return {"error": str(e)}, 400

    # @jwt_required()
    def delete(self, endereco_id):
        endereco_service = EnderecoService(db.session)
        try:
            endereco_service.deletar_endereco(endereco_id)
            return {"msg": "Endereco deletado com sucesso"}, 200
        except Exception as e:
            return {"error": str(e)}, 400
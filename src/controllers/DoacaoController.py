from flask_restful import Resource, reqparse
from src.services.DoacaoService import DoacaoService
from src.models.Base import db
from flask import request
import traceback

doacao_create_parser = reqparse.RequestParser()
doacao_create_parser.add_argument('doador_id', type=str, required=True)
doacao_create_parser.add_argument('solicitante_id', type=str, required=False)
doacao_create_parser.add_argument('descricao', type=str, required=False)
doacao_create_parser.add_argument('status_id', type=str, required=True)
doacao_create_parser.add_argument('data_recebimento', type=str, required=False)

doacao_update_parser = reqparse.RequestParser()
doacao_update_parser.add_argument('doador_id', type=str, required=False)
doacao_update_parser.add_argument('solicitante_id', type=str, required=False)
doacao_update_parser.add_argument('descricao', type=str, required=False)
doacao_update_parser.add_argument('status_id', type=str, required=False)
doacao_update_parser.add_argument('data_recebimento', type=str, required=False)


class DoacaoListResource(Resource):
    #@jwt_required()
    def get(self):
        try:
            doacao_service = DoacaoService(db.session)
            doacoes = doacao_service.listar_todos()
            result = []
            for d in doacoes:
                doacao_dict = {
                    "id": d.id,
                    "doador_nome": d.doador.nome,
                    "solicitante_nome": d.doador.nome,
                    "descricao": d.descricao,
                    "status_id": d.status.nome,
                    "dataDoacao": d.dataDoacao.isoformat() if d.dataDoacao else None,
                    "data_recebimento": d.data_recebimento.isoformat() if d.data_recebimento else None
                }
                result.append(doacao_dict)
            return result, 200
        except Exception as e:
            print("Erro ao buscar doacoes:", e)
            traceback.print_exc()
            return {"error": str(e)}, 500

    def post(self):
        data = request.get_json()
        doacao_service = DoacaoService(db.session)
        try:
            doacao = doacao_service.criar_doacao(data)
            return {"id": doacao.id, "msg": "Doacao adicionado com sucesso"}, 201
        except Exception as e:
            return {"error": str(e)}, 400
        
class DoacoesPorSolicitanteResource(Resource):
    def get(self, user_id):
        doacao_service = DoacaoService(db.session)
        try:
            doacoes = doacao_service.listar_por_solicitante_id(user_id)
            return [
                {
                    "id": d.id,
                    "descricao": d.descricao,
                    "status_id": d.status.nome,
                    "dataDoacao": d.dataDoacao.isoformat() if d.dataDoacao else None,
                    "doador_nome": d.doador.nome,
                    "data_recebimento": d.data_recebimento.isoformat() if d.data_recebimento else None
                }
                for d in doacoes
            ], 200
        except Exception as e:
            return {"error": str(e)}, 500
        
class DoacoesPorDoadorResource(Resource):
    def get(self, user_id):
        doacao_service = DoacaoService(db.session)
        try:
            doacoes = doacao_service.listar_por_doador_id(user_id)
            return [
                {
                    "id": d.id,
                    "descricao": d.descricao,
                    "status_id": d.status.nome,
                    "dataDoacao": d.dataDoacao.isoformat() if d.dataDoacao else None,
                    "solicitante_nome": d.solicitante.nome,
                    "data_recebimento": d.data_recebimento.isoformat() if d.data_recebimento else None
                }
                for d in doacoes
            ], 200
        except Exception as e:
            return {"error": str(e)}, 500


class DoacaoResource(Resource):
    # @jwt_required()
    def get(self, doacao_id):
        try:
            doacao_service = DoacaoService(db.session)
            doacao = doacao_service.listar_por_id(doacao_id)
            if not doacao:
                return {"msg": "Doacao não encontrado"}, 404
            return {
                    "doador_nome": doacao.doador.nome,
                    "solicitante_nome": doacao.doador.nome,
                    "descricao": doacao.descricao,
                    "status_id": doacao.status.nome,
                    "dataDoacao": doacao.dataDoacao.isoformat() if doacao.dataDoacao else None,
                    "data_recebimento": doacao.data_recebimento.isoformat() if doacao.data_recebimento else None
            }, 200
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"error": str(e)}, 500

    # @jwt_required()
    def put(self, doacao_id):
        args = doacao_update_parser.parse_args()
        doacao_service = DoacaoService(db.session)
        try:
            doacao = doacao_service.atualizar_doacao(doacao_id, args)
            data = request.get_json()
            print("Dados recebidos do request:", data)
            return {"msg": "Doacao atualizado com sucesso"}, 200
        except Exception as e:
            return {"error": str(e)}, 400

    # @jwt_required()
    def delete(self, doacao_id):
        doacao_service = DoacaoService(db.session)
        try:
            doacao_service.deletar_doacao(doacao_id)
            return {"msg": "Doacao deletado com sucesso"}, 200
        except Exception as e:
            return {"error": str(e)}, 400
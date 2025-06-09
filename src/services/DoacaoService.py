import re
from src.models.Doacao import Doacao
from src.repositories.DoacaoRepository import DoacaoRepository
from sqlalchemy.orm import Session
from datetime import datetime

class DoacaoService:
    def __init__(self, session: Session):
        self.repo = DoacaoRepository(session)
        self.session = session

    def listar_todos(self):
        return self.repo.get_all()

    def listar_por_id(self, doacao_id):
        return self.repo.get_by_id(doacao_id)
    
    def listar_por_doador_id(self, doador_id):
        return self.repo.get_by_doador_id(doador_id)
    
    def listar_por_solicitante_id(self, solicitante_id):
        return self.repo.get_by_solicitante_id(solicitante_id)

    def criar_doacao(self, data):
        campos_obrigatorios = ["doador_id", "status_id"]
        campos_faltando = [campo for campo in campos_obrigatorios if not data.get(campo)]

        if campos_faltando:
            raise ValueError(f"Campos obrigatórios faltando: {', '.join(campos_faltando)}")

        doador_id = data.get("doador_id")
        if not self.user_repo.get_by_id(doador_id):
            raise ValueError(f"Doador com ID {doador_id} não existe.")
        
        status_id = data["status_id"]
        if not self.status_repo.get_by_id(status_id):
            raise ValueError(f"Status com ID {status_id} não existe.")
        
        solicitante_id = data.get("solicitante_id")
        if solicitante_id and not self.user_repo.get_by_id(solicitante_id):
            raise ValueError(f"Solicitante com ID {solicitante_id} não existe.")

        doacao = Doacao(
            doador_id=doador_id,
            status_id=status_id,
            dataDoacao=datetime(),
            solicitante_id=solicitante_id,
            descricao=data.get("descricao"),
            data_recebimento=data.get("data_recebimento"),
        )

        return self.repo.add(doacao)


    def atualizar_doacao(self, doacao_id, data):
        doacao = self.repo.get_by_id(doacao_id)

        print("Dados recebidos para atualização:", data)

        if not doacao:
            raise ValueError("Doação não encontrada.")

        if "descricao" in data and data["descricao"] is not None:
            doacao.descricao = data["descricao"]

        if "solicitante_id" in data and data["solicitante_id"] is not None:
            solicitante_id = data["solicitante_id"]
            if not self.user_repo.get_by_id(solicitante_id):
                raise ValueError(f"Solicitante com ID {solicitante_id} não existe.")
            
            doacao.solicitante_id = solicitante_id

        if "status_id" in data and data["status_id"] is not None:
            status_id = data["status_id"]
            if not self.status_repo.get_by_id(status_id):
                raise ValueError(f"Status com ID {status_id} não existe.")
            
            doacao.status_id = status_id

        if "data_recebimento" in data and data["data_recebimento"] is not None:
            doacao.data_recebimento = data["data_recebimento"]

        self.repo.update()
        
        return doacao



    def deletar_doacao(self, doacao_id):
        doacao = self.repo.get_by_id(doacao_id)
        if not doacao:
            raise ValueError("Doacao não encontrado.")

        self.repo.delete(doacao)
        return True
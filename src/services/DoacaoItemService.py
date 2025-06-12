import re
from src.models.Doacao_item import DoacaoItem
from src.repositories.DoacaoItemRepository import DoacaoItemRepository
from src.repositories.DoacaoRepository import DoacaoRepository
from src.repositories.AlimentoRepository import AlimentoRepository
from sqlalchemy.orm import Session
from datetime import datetime

class DoacaoItemService:
    def __init__(self, session: Session):
        self.repo = DoacaoItemRepository(session)
        self.doacao_repo = DoacaoRepository(session)
        self.alimento_repo = AlimentoRepository(session)
        self.session = session

    def listar_todos(self):
        return self.repo.get_all()

    def listar_por_id(self, doacao_id):
        return self.repo.get_by_id(doacao_id)
    
    def criar_doacaoItem(self, data):
        campos_obrigatorios = ["doacao_id", "alimento_id", "quantidade", "data_vencimento"]
        campos_faltando = [campo for campo in campos_obrigatorios if not data.get(campo)]

        if campos_faltando:
            raise ValueError(f"Campos obrigatórios faltando: {', '.join(campos_faltando)}")

        doacao_id = data.get("doacao_id")
        if not self.doacao_repo.get_by_id(doacao_id):
            raise ValueError(f"Doacao com ID {doacao_id} não existe.")
        
        alimento_id = data.get("alimento_id")
        if not self.alimento_repo.get_by_id(alimento_id):
            raise ValueError(f"Alimento com ID {alimento_id} não existe.")

        quantidade = data["quantidade"]
        if quantidade <= 0:
            raise ValueError(f"Quantidade deve ser maior que 0")
        
        dataVencimento_str = data["data_vencimento"] 
        data_vencimento = datetime.strptime(dataVencimento_str, "%Y-%m-%d")
        data_atual = datetime.now()

        if data_vencimento < data_atual:
            raise ValueError("A data de vencimento deve ser maior que a data atual")

        doacaoItem = DoacaoItem(
            doacao_id = doacao_id,
            alimento_id = alimento_id,
            quantidade = quantidade,
            data_vencimento=data_vencimento,
        )

        return self.repo.add(doacaoItem)

    def atualizar_doacaoItem(self, doacaoItem_id, data):
        doacaoItem = self.repo.get_by_id(doacaoItem_id)

        print("Dados recebidos para atualização:", data)

        if not doacaoItem:
            raise ValueError("DoaçãoItem não encontrada.")

        if "doacao_id" in data and data["doacao_id"] is not None:
            doacao_id = data["doacao_id"]
            if not self.doacao_repo.get_by_id(doacao_id):
                raise ValueError(f"Doacao com ID {doacao_id} não existe.")

            doacaoItem.doacao_id = doacao_id

        if "alimento_id" in data and data["alimento_id"] is not None:
            alimento_id = data["alimento_id"]
            if not self.alimento_repo.get_by_id(alimento_id):
                raise ValueError(f"Alimento com ID {alimento_id} não existe.")

            doacaoItem.alimento_id = alimento_id

        if "quantidade" in data and data["quantidade"] is not None:
            quantidade = int(data["quantidade"])
            if quantidade <= 0:
                raise ValueError(f"Quantidade deve ser maior que 0")
            doacaoItem.quantidade = quantidade

        if "data_vencimento" in data and data["data_vencimento"] is not None:
            data_vencimento_str = data["data_vencimento"]
            data_vencimento = datetime.strptime(data_vencimento_str, "%Y-%m-%d")
            data_atual = datetime.now()

            if data_vencimento < data_atual:
                raise ValueError("A data de vencimento deve ser maior que a data atual")

            doacaoItem.data_vencimento = data_vencimento

        self.repo.update()

        return doacaoItem

    def deletar_doacaoItem(self, doacaoItem_id):
        doacaoItem = self.repo.get_by_id(doacaoItem_id)
        if not doacaoItem:
            raise ValueError("DoacaoItem não encontrado.")

        self.repo.delete(doacaoItem)
        return True
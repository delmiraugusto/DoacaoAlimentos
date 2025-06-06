import re
from src.models.Status import Status
from src.repositories.StatusRepository import StatusRepository
from sqlalchemy.orm import Session

class StatusService:
    def __init__(self, session: Session):
        self.repo = StatusRepository(session)
        self.session = session

    def listar_todos(self):
        return self.repo.get_all()

    def listar_por_id(self, status_id):
        return self.repo.get_by_id(status_id)

    def criar_status(self, data):
        campos_obrigatorios = ["nome"]
        campos_faltando = [campo for campo in campos_obrigatorios if not data.get(campo)]

        if campos_faltando:
            raise ValueError(f"Campos obrigatórios faltando: {', '.join(campos_faltando)}")

        nome = data.get("nome")
        if not nome :
            raise ValueError("Nome não pode estar vazia.")
        
        if not re.match(r"^[A-Za-zÀ-ÿ\s\-]+$", nome):
            raise ValueError("Nome contém caracteres inválidos.")
        
        
        
        status = Status(
            nome=nome,
        )

        return self.repo.add(status)


    def atualizar_status(self, status_id, data):
        status = self.repo.get_by_id(status_id)

        print("Dados recebidos para atualização:", data)

        if not status:
            raise ValueError("Status não encontrado.")

        if "nome" in data and data["nome"]:
            status.nome = data["nome"]

        self.repo.update()
        return status

    def deletar_status(self, status_id):
        status = self.repo.get_by_id(status_id)
        if not status:
            raise ValueError("Status não encontrado.")

        self.repo.delete(status)
        return True
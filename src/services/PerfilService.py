import re
from src.models.Perfil import Perfil
from src.repositories.PerfilRepository import PerfilRepository
from sqlalchemy.orm import Session

class PerfilService:
    def __init__(self, session: Session):
        self.repo = PerfilRepository(session)
        self.session = session

    def listar_todos(self):
        return self.repo.get_all()

    def listar_por_id(self, perfil_id):
        return self.repo.get_by_id(perfil_id)

    def criar_perfil(self, data):
        campos_obrigatorios = ["nome"]
        campos_faltando = [campo for campo in campos_obrigatorios if not data.get(campo)]

        if campos_faltando:
            raise ValueError(f"Campos obrigatórios faltando: {', '.join(campos_faltando)}")

        nome = data.get("nome")
        if not nome :
            raise ValueError("Nome não pode estar vazia.")
        
        if not re.match(r"^[A-Za-zÀ-ÿ\s\-]+$", nome):
            raise ValueError("Nome contém caracteres inválidos.")
        
        perfil = Perfil(
            nome=nome,
        )

        return self.repo.add(perfil)


    def atualizar_perfil(self, perfil_id, data):
        perfil = self.repo.get_by_id(perfil_id)

        print("Dados recebidos para atualização:", data)

        if not perfil:
            raise ValueError("Perfil não encontrado.")

        if "nome" in data and data["nome"]:
            perfil.nome = data["nome"]

        self.repo.update()
        return perfil

    def deletar_perfil(self, perfil_id):
        perfil = self.repo.get_by_id(perfil_id)
        if not perfil:
            raise ValueError("Perfil não encontrado.")

        self.repo.delete(perfil)
        return True
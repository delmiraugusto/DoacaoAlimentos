import re
from src.models.Alimento import Alimento
from src.repositories.AlimentoRepository import AlimentoRepository
from sqlalchemy.orm import Session

class AlimentoService:
    def __init__(self, session: Session):
        self.repo = AlimentoRepository(session)
        self.session = session

    def listar_todos(self):
        return self.repo.get_all()

    def listar_por_id(self, alimento_id):
        return self.repo.get_by_id(alimento_id)

    def criar_alimento(self, data):
        campos_obrigatorios = ["nome", "marca"]
        campos_faltando = [campo for campo in campos_obrigatorios if not data.get(campo)]

        if campos_faltando:
            raise ValueError(f"Campos obrigatórios faltando: {', '.join(campos_faltando)}")

        nome = data.get("nome")
        if not nome :
            raise ValueError("Nome não pode estar vazia.")
        
        if not re.match(r"^[A-Za-zÀ-ÿ\s\-]+$", nome):
            raise ValueError("Nome contém caracteres inválidos.")
        
        marca = data.get("marca")
        if not nome :
            raise ValueError("Marca não pode estar vazia.")
        
        alimento = Alimento(
            nome=data.get("nome"),
            marca=marca,
        )

        return self.repo.add(alimento)


    def atualizar_alimentos(self, alimento_id, data):
        alimento = self.repo.get_by_id(alimento_id)

        print("Dados recebidos para atualização:", data)

        if not alimento:
            raise ValueError("Alimento não encontrado.")

        if "nome" in data and data["nome"]:
            alimento.nome = data["nome"]
        if "marca" in data and data["marca"]:
            alimento.marca = data["marca"]

        self.repo.update()
        return alimento

    def deletar_alimento(self, alimento_id):
        alimento = self.repo.get_by_id(alimento_id)
        if not alimento:
            raise ValueError("Alimento não encontrado.")

        self.repo.delete(alimento)
        return True
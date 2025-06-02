import re
from src.models.Users import Users
from src.models.Perfil import Perfil 
from src.models.Doacao import Doacao
from src.repositories.UsersRepository import UserRepository
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError

bcrypt = Bcrypt()

VALID_PROFILES = ['doador', 'solicitante']

def validar_telefone(telefone):
    return re.fullmatch(r'\+?\d{8,15}', telefone) is not None

def validar_documento(documento):
    return documento is not None and len(documento) >= 5

class UserService:
    def __init__(self, session: Session):
        self.repo = UserRepository(session)
        self.session = session

    def listar_todos(self):
        return self.repo.get_all()

    def listar_por_id(self, user_id):
        return self.repo.get_by_id(user_id)

    def listar_por_email(self, email):
        return self.repo.get_by_email(email)

    def criar_usuario(self, data):
        perfil_nome = data.get("perfil")
        perfil = self.session.query(Perfil).filter(Perfil.nome.ilike(perfil_nome)).first()
        if not perfil or perfil.nome.lower() not in VALID_PROFILES:
            raise ValueError("Perfil inválido. Deve ser 'doador' ou 'solicitante'.")

        telefone = data.get("telefone")
        if not validar_telefone(telefone):
            raise ValueError("Telefone inválido.")

        email = data.get("email")
        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError:
            raise ValueError("Email inválido.")

        documento = data.get("documento")
        if not validar_documento(documento):
            raise ValueError("Documento inválido.")

        if self.repo.get_by_email(email):
            raise ValueError("Email já cadastrado.")

        senha = data.get("senha")
        senha_hash = bcrypt.generate_password_hash(senha).decode('utf-8')

        user = Users(
            nome=data.get("nome"),
            email=email,
            senha_hash=senha_hash,
            telefone=telefone,
            documento=documento,
            perfil_id=perfil.id,
            endereco_id=data.get("endereco_id"),
            numero=data.get("numero"),
            complemento=data.get("complemento"),
        )

        return self.repo.add(user)

    def atualizar_usuario(self, user_id, data):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")

        if "nome" in data:
            user.nome = data["nome"]
        if "telefone" in data and validar_telefone(data["telefone"]):
            user.telefone = data["telefone"]
        if "documento" in data and validar_documento(data["documento"]):
            user.documento = data["documento"]
        if "endereco_id" in data:
            user.endereco_id = data["endereco_id"]
        if "numero" in data:
            user.numero = data["numero"]
        if "complemento" in data:
            user.complemento = data["complemento"]

        self.repo.update()
        return user

    def deletar_usuario(self, user_id):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")

        doacoes_pendentes = self.session.query(Doacao).filter(
            Doacao.doador_id == user_id,
            Doacao.status.has(Doacao.status.has(Doacao.status_id.in_([1,2]))) 
        ).count()

        if doacoes_pendentes > 0:
            raise ValueError("Usuário possui doações pendentes ou em andamento e não pode ser deletado.")

        self.repo.delete(user)
        return True

    def autenticar(self, email, senha):
        user = self.repo.get_by_email(email)
        if not user:
            return None

        if bcrypt.check_password_hash(user.senha_hash, senha):
            return user

        return None

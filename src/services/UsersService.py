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
        campos_obrigatorios = ["nome", "email", "senha", "telefone", "documento", "perfil_id", "endereco_id", "numero"]
        campos_faltando = [campo for campo in campos_obrigatorios if not data.get(campo)]

        if campos_faltando:
            raise ValueError(f"Campos obrigatórios faltando: {', '.join(campos_faltando)}")
        perfil_id = data.get("perfil_id")
        if not perfil_id:
            raise ValueError("Campo 'perfil_id' é obrigatório.")

        perfil = self.session.query(Perfil).filter(Perfil.id == perfil_id).first()
        if not perfil:
            raise ValueError("Perfil não encontrado.")

        if perfil.nome.lower() not in VALID_PROFILES:
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
        if not senha or len(senha) < 8:
            raise ValueError("Senha não pode estar vazia.")
        
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

        print("Dados recebidos para atualização:", data)

        if not user:
            raise ValueError("Usuário não encontrado.")

        if "nome" in data and data["nome"]:
            user.nome = data["nome"]
        if "senha" in data and data["senha"]:
            senha = data["senha"]
            if len(senha) < 8:
                raise ValueError("Senha deve ter no mínimo 8 caracteres.")
            user.senha_hash = bcrypt.generate_password_hash(senha).decode('utf-8')
        if "telefone" in data and data["telefone"] and validar_telefone(data["telefone"]):
            user.telefone = data["telefone"]
        if "documento" in data and data["documento"] and validar_documento(data["documento"]):
            user.documento = data["documento"]
        if "endereco_id" in data and data["endereco_id"]:
            user.endereco_id = data["endereco_id"]
        if "numero" in data and data["numero"]:
            user.numero = data["numero"]
        if "complemento" in data and data["complemento"]:
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

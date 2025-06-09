from src.models.Users import Users
from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(Users).all()

    def get_by_id(self, user_id):
        return self.session.query(Users).filter(Users.id == user_id).first()

    def get_by_email(self, email):
        return self.session.query(Users).filter(Users.email == email).first()
    
    def isDoador(self, user_id):
        user = self.session.query(Users).filter(Users.id == user_id).first()
        if not user:
            raise ValueError("Usuário não encontrado")
        if user.perfil_id == 1:
            return True
        else:
            raise ValueError("Não é doador")
        
    def isSolicitante(self, user_id):
        user = self.session.query(Users).filter(Users.id == user_id).first()
        if not user:
            raise ValueError("Usuário não encontrado")
        if user.perfil_id == 2:
            return True
        else:
            raise ValueError("Não é solicitante")
    
    def add(self, user):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update(self):
        self.session.commit()

    def delete(self, user):
        self.session.delete(user)
        self.session.commit()

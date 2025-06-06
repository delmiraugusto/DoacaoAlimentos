from src.models.Perfil import Perfil
from sqlalchemy.orm import Session

class PerfilRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(Perfil).all()

    def get_by_id(self, perfil_id):
        return self.session.query(Perfil).filter(Perfil.id == perfil_id).first()

    def add(self, perfil):
        self.session.add(perfil)
        self.session.commit()
        self.session.refresh(perfil)
        return perfil

    def update(self):
        self.session.commit()

    def delete(self, perfil):
        self.session.delete(perfil)
        self.session.commit()
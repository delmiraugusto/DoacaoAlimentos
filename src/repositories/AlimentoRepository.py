from src.models.Alimento import Alimento
from sqlalchemy.orm import Session

class AlimentoRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(Alimento).all()

    def get_by_id(self, alimento_id):
        return self.session.query(Alimento).filter(Alimento.id == alimento_id).first()

    def add(self, alimento):
        self.session.add(alimento)
        self.session.commit()
        self.session.refresh(alimento)
        return alimento

    def update(self):
        self.session.commit()

    def delete(self, alimento):
        self.session.delete(alimento)
        self.session.commit()

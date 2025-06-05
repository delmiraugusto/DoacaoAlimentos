from src.models.Status import Status
from sqlalchemy.orm import Session

class AlimentoRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(Status).all()

    def get_by_id(self, status_id):
        return self.session.query(Status).filter(Status.id == status_id).first()

    def add(self, status):
        self.session.add(status)
        self.session.commit()
        self.session.refresh(status)
        return status

    def update(self):
        self.session.commit()

    def delete(self, status):
        self.session.delete(status)
        self.session.commit()
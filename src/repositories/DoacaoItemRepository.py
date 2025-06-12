from src.models.Doacao_item import DoacaoItem
from sqlalchemy.orm import Session

class DoacaoItemRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(DoacaoItem).all()

    def get_by_id(self, doacaoItem_id):
        return self.session.query(DoacaoItem).filter(DoacaoItem.id == doacaoItem_id).first()

    def add(self, doacaoItem):
        self.session.add(doacaoItem)
        self.session.commit()
        self.session.refresh(doacaoItem)
        return doacaoItem

    def update(self):
        self.session.commit()

    def delete(self, doacaoItem):
        self.session.delete(doacaoItem)
        self.session.commit()
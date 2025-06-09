from src.models.Doacao import Doacao
from sqlalchemy.orm import Session

class DoacaoRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(Doacao).all()

    def get_by_id(self, doacao_id):
        return self.session.query(Doacao).filter(Doacao.id == doacao_id).first()
    
    def get_by_doador_id(self, doador_id):
        return self.session.query(Doacao).filter(Doacao.doador_id == doador_id).all()

    def get_by_solicitante_id(self, solicitante_id):
        return self.session.query(Doacao).filter(Doacao.solicitante_id == solicitante_id).all()

    def add(self, doacao):
        self.session.add(doacao)
        self.session.commit()
        self.session.refresh(doacao)
        return doacao

    def update(self):
        self.session.commit()

    def delete(self, doacao):
        self.session.delete(doacao)
        self.session.commit()

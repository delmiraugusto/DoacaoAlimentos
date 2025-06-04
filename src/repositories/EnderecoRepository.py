from src.models.Endereco import Endereco
from sqlalchemy.orm import Session

class EnderecoRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(Endereco).all()
    
    def get_by_fields(self, cep, logradouro, bairro, cidade, uf):
        return self.session.query(Endereco).filter_by(
        cep=cep,
        logradouro=logradouro,
        bairro=bairro,
        cidade=cidade,
        uf=uf
    ).first()

    def get_by_id(self, endereco_id):
        return self.session.query(Endereco).filter(Endereco.id == endereco_id).first()
    
    def get_by_cep(self, cep):
        return self.session.query(Endereco).filter(Endereco.cep == cep).first()

    def add(self, endereco: Endereco):
        self.session.add(endereco)
        self.session.commit()
        self.session.refresh(endereco)
        return endereco

    def update(self):
        self.session.commit()

    def delete(self, alimento):
        self.session.delete(alimento)
        self.session.commit()

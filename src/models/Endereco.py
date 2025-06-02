from sqlalchemy import Column, BigInteger, String
from .Base import Base

class Endereco(Base):
    __tablename__ = "endereco"

    id = Column(BigInteger, primary_key=True)
    cep = Column(String(9))
    logradouro = Column(String(100))
    bairro = Column(String(100))
    uf = Column(String(2))
    cidade = Column(String(100))
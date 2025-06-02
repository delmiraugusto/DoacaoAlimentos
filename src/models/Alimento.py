from sqlalchemy import Column, BigInteger, String
from .Base import Base

class Alimento(Base):
    __tablename__ = "alimento"

    id = Column(BigInteger, primary_key=True)
    nome = Column(String(50), nullable=False)
    marca = Column(String(50))
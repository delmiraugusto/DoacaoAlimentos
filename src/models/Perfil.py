from sqlalchemy import Column, BigInteger, String
from .Base import Base

class Perfil(Base):
    __tablename__ = "perfil"

    id = Column(BigInteger, primary_key=True)
    nome = Column(String(50))

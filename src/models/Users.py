from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from .Base import Base
from .Endereco import Endereco
from .Status import Status


class Users(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    nome = Column(String(100))
    email = Column(String(50), nullable=False, unique=True)
    senha_hash = Column(String(100), nullable=False)
    telefone = Column(String(30), nullable=False)
    documento = Column(String(20), nullable=False)
    numero = Column(String(20))
    complemento = Column(String(100))

    perfil_id = Column(BigInteger, ForeignKey("perfil.id", ondelete="RESTRICT"), nullable=False)
    endereco_id = Column(BigInteger, ForeignKey("endereco.id", ondelete="SET NULL"), nullable=True)

    perfil = relationship("Perfil")
    endereco = relationship("Endereco")

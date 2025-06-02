from sqlalchemy import Column, BigInteger, String
from .Base import Base

class Status(Base):
    __tablename__ = "status"

    id = Column(BigInteger, primary_key=True)
    nome = Column(String(30))

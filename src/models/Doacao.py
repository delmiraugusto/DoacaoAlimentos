from sqlalchemy import Column, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .Base import Base

class Doacao(Base):
    __tablename__ = "doacao"

    id = Column(BigInteger, primary_key=True)
    doador_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    solicitante_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    dataDoacao = Column(DateTime, nullable=False)
    status_id = Column(BigInteger, ForeignKey("status.id"), nullable=False)
    data_recebimento = Column(DateTime)

    doador = relationship("Users", foreign_keys=[doador_id])
    solicitante = relationship("Users", foreign_keys=[solicitante_id])
    status = relationship("Status")

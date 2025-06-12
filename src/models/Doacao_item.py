from sqlalchemy import Column, BigInteger, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from .Base import Base

class DoacaoItem(Base):
    __tablename__ = "doacaoitem"

    id = Column(BigInteger, primary_key=True)
    doacao_id = Column(BigInteger, ForeignKey("doacao.id"), nullable=False)
    alimento_id = Column(BigInteger, ForeignKey("alimento.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    data_vencimento = Column(Date)

    doacao = relationship("Doacao")
    alimento = relationship("Alimento")
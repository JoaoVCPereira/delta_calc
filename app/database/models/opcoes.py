from datetime import datetime

from database.connection import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey,Float
from sqlalchemy.orm import relationship,validates
from schemas.opcoes import OpcoesDB as OpcoesDB

class Opcoes(Base):
    __tablename__ = 'opcoes'

    opcao_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticket = Column(String, nullable=False)
    stock_price = Column(Float, nullable=False)
    strike_price = Column(Float, nullable=False)
    opcao_price = Column(Float,nullable=False)
    selic = Column(Float, nullable=False)
    operation_type = Column(String(4), nullable=False)
    execution_date = Column(DateTime(timezone=True), nullable=False)
    implicit_vol = Column(Float, nullable=False)
    delta = Column(Float, nullable=False)
    boleta_id = Column(Integer, ForeignKey('boletas.boleta_id', ondelete='SET NULL'), nullable=True)

    boleta = relationship("Boletas", back_populates="opcoes")

    def from_schema(self, schema: OpcoesDB):
        self.ticket = schema.ticket
        self.stock_price = schema.stock_price
        self.strike_price = schema.strike_price
        self.opcao_price = schema.opcao_price
        self.selic = schema.selic
        self.operation_type = schema.operation_type
        self.execution_date = schema.execution_date
        self.implicit_vol = schema.implicit_vol
        self.delta = schema.delta
        self.boleta_id = schema.boleta_id
        return self

    def to_schema(self) -> OpcoesDB:
        return OpcoesDB(
            opcao_id=self.opcao_id,
            ticket=self.ticket,
            stock_price=self.stock_price,
            strike_price=self.strike_price,
            opcao_price=self.opcao_price,
            selic=self.selic,
            operation_type=self.operation_type,
            execution_date=self.execution_date,
            implicit_vol=self.implicit_vol,
            delta=self.delta,
            created=self.created,
            updated=self.updated,
            boleta_id=self.boleta_id
        )
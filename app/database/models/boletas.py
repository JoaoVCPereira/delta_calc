from datetime import datetime

from database.connection import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey,Float
from sqlalchemy.orm import relationship,validates
from schemas.boletas import BoletasDB as BoletasDB

class Boletas(Base):
    __tablename__ = 'boletas'

    boleta_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    overall_delta = Column(Float, nullable=False)
    opcoes = relationship("Opcoes", back_populates="boleta", cascade="all, delete-orphan")

    def from_schema(self, schema: BoletasDB):
        self.overall_delta = schema.overall_delta
        return self

    def to_schema(self) -> BoletasDB:
        return BoletasDB(
            boleta_id=self.boleta_id,
            overall_delta=self.overall_delta,
            created=self.created,
            updated=self.updated
        )
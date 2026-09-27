from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OpcoesDB(BaseModel):
    opcao_id: Optional[int] = None
    ticket: str
    stock_price: float
    strike_price: float
    opcao_price: float
    selic: float
    operation_type: str
    execution_date: datetime
    implicit_vol: float
    delta: float    
    boleta_id: Optional[int] = None
    created: Optional[datetime]=None
    updated: Optional[datetime]=None
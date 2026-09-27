from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BoletasDB(BaseModel):
    boleta_id: Optional[int] = None
    overall_delta: float

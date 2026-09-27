from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BoletasDB(BaseModel):
    boleta_id: Optional[int] = None
    created: Optional[datetime]=None
    updated: Optional[datetime]=None
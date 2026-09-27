from pydantic import BaseModel

class Response(BaseModel):
    status:bool | None = False
    error:bool | None = False
    code:int | None = None
    reference:str | None = None
    message:str | None = None
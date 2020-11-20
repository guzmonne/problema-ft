from typing import Optional
from pydantic import BaseModel

class ValueStruct(BaseModel):
    number: int
    unit: str
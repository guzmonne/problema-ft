from typing import Optional
from pydantic import BaseModel

from .value_struct import ValueStruct

class Value(BaseModel):
    id: Optional[str]
    name: str
    struct: Optional[ValueStruct]
    natural_language: Optional[str]
from typing import Optional, List
from pydantic import BaseModel

from .value_struct import ValueStruct
from .value import Value

class Attribute(BaseModel):
    id: str
    name: str
    value_id: Optional[str]
    value_name: Optional[str]
    value_type: Optional[str]
    value_struct: Optional[ValueStruct]
    values: Optional[List[Value]]
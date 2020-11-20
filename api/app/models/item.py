from typing import Optional, List
from pydantic import BaseModel

from .attribute import Attribute

class Item(BaseModel):
    id: str
    attributes: Optional[List[Attribute]]
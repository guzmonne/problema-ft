from typing import List
from pydantic import BaseModel

from .component import Component

class Group(BaseModel):
    id: str
    label: str
    section: str
    components: List[Component]
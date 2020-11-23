from typing import List
from pydantic import BaseModel

from .group import Group

class FT(BaseModel):
    id: str
    domain: str
    groups: List[Group]
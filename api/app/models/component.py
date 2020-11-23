from typing import Optional, List
from pydantic import BaseModel

from .attribute import Attribute


class Component(BaseModel):
    component: str
    label: str
    attributes: List[Attribute]
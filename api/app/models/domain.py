from typing import List
from pydantic import BaseModel

from .group import Group

class Domain(BaseModel):
    main_title: str
    groups: List[Group]
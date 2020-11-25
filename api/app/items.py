from typing import List, Dict

from .exceptions import CustomException
from .meli import Meli
from .utils import safe_get, identity, add_natural_language
from .models.component import Component
from .models.attribute import Attribute
from .models.group import Group
from .models.item import Item
from .models.domain import Domain


OUTPUT_TRANSFORMS = dict(
    TEXT_OUTPUT=identity,
    NUMBER_OUTPUT=identity,
    BOOLEAN_OUTPUT=identity,
    NUMBER_UNIT_OUTPUT=add_natural_language,
)

class Items(object):
    def __init__(self):
        self.meli = Meli()

    def get_meli_item_for_id(self, item_id: str) -> Item:
        item = self.meli.get_item(item_id)
        if item is None:
            raise ItemNotFound(item_id)
        return item

    def get_meli_domain_for_item(self, item: Item) -> Domain:
        domain_id = item.get('domain_id')
        if domain_id == None:
            raise UndefinedDomainID(item)
        domain = self.meli.get_domain(domain_id)
        if domain is None:
            raise DomainNotFound(domain_id)
        return domain

    def merge_attributes(self, item_attributes_dict: Dict[str, Attribute], attributes: List[Attribute], value_transform=identity) -> List[Attribute]:
        result = []
        for attribute in attributes:
            attribute_id = attribute.get("id", "")
            item_attribute = item_attributes_dict.get(attribute_id)
            if item_attribute is None:
                continue
            result.append(dict(
                id=attribute.get("id", ""),
                name=attribute.get("name", ""),
                value_id=item_attribute.get("value_id", ""),
                value_name=item_attribute.get("value_name", ""),
                value_type=attribute.get("value_type", ""),
                value=value_transform(
                    safe_get(item_attribute.get("values"), 0)
                ),
            ))
        return result

    def merge_components(self, item_attributes_dict: Dict[str, Attribute], components: List[Component]) -> List[Component]:
        result = []
        for component in components:
            transform = OUTPUT_TRANSFORMS.get(component.get("component"))
            if transform is None:
                continue
            attributes = self.merge_attributes(item_attributes_dict, component.get("attributes"), value_transform=transform)
            if len(attributes) == 0:
                continue
            result.append(dict(
                component=component.get("component"),
                label=component.get("label"),
                attributes=attributes,
            ))
        return result

    def merge_groups(self, item_attributes_dict: Dict[str, Attribute], groups: List[Group]) -> List[Group]:
        result = []
        for group in groups:
            components = self.merge_components(item_attributes_dict, group.get("components", []))
            result.append(dict(
                id=group.get("id", ""),
                label=group.get("label", ""),
                section=group.get("section", ""), 
                components=components,
            ))
        return result

    def get_item_attributes_dict(self, item: Item) -> Dict[str, Attribute]:
        attributes = item.get("attributes", [])
        return {attribute["id"]: attribute for attribute in attributes}

    def get_item(self, item_id: str):
        item = self.get_meli_item_for_id(item_id)
        domain = self.get_meli_domain_for_item(item)
        item_attributes_dict = self.get_item_attributes_dict(item)
        groups = self.merge_groups(item_attributes_dict, domain.get("groups", []))
        return dict(
            id=item_id,
            domain=item.get("domain_id"),
            groups=groups,
        )


class UndefinedDomainID(CustomException):
    def init(self, item):
        self.item = item
        return f"Domain ID is undefined on item {item.get('id')}"

class ItemNotFound(CustomException):
    def init(self, item_id):
        self.item_id = item_id
        return f"An item with id {item_id} was not found"

class DomainNotFound(CustomException):
    def init(self, domain_id):
        self.domain_id = domain_id
        return f"A domain with id {domain_id} was not found"

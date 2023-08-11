from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class MenuSchemaBase(BaseModel):
    title: str
    description: str


class MenuSchemaIn(MenuSchemaBase):
    pass


class MenuSchemaOut(MenuSchemaBase, SchemaBase):
    submenus_count: int
    dishes_count: int


class SubmenuSchemaIn(BaseModel):
    title: str
    description: str


class SubmenuSchemaOut(SubmenuSchemaIn, SchemaBase):
    dishes_count: int


class DishSchemaIn(BaseModel):
    title: str
    description: str
    price: Decimal


class DishSchemaOut(DishSchemaIn, SchemaBase):
    pass


class CatalogSubmenuItemSchema(SchemaBase):
    title: str
    description: str
    dishes: list[DishSchemaOut]


class MenuCatalogSchemaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    submenus: list[CatalogSubmenuItemSchema]

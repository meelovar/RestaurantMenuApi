from __future__ import annotations

import uuid
from decimal import Decimal
from typing import List

from sqlalchemy import (
    DECIMAL,
    ForeignKey,
    String,
    UUID,
    func,
    select,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    column_property,
    mapped_column,
    relationship,
)


class BaseModel(DeclarativeBase):
    """Base model"""
    id: Mapped[uuid.UUID]


class Dish(BaseModel):
    """Dish model"""
    __tablename__ = "dish"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(300))
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    submenu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("submenu.id", ondelete="CASCADE"))
    submenu: Mapped[Submenu] = relationship(back_populates="dishes")


class Submenu(BaseModel):
    """Submenu model"""
    __tablename__ = "submenu"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(200))
    menu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("menu.id", ondelete="CASCADE"))
    menu: Mapped[Menu] = relationship(back_populates="submenus")
    dishes: Mapped[List[Dish]] = relationship(back_populates="submenu", cascade="all, delete")
    dishes_count: Mapped[int] = column_property(
        select(func.count(Dish.id)).filter(Dish.submenu_id == id).scalar_subquery()
    )


class Menu(BaseModel):
    """Menu model"""
    __tablename__ = "menu"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(200))
    submenus: Mapped[List[Submenu]] = relationship(back_populates="menu", cascade="all, delete")
    submenus_count: Mapped[int] = column_property(
        select(func.count(Submenu.id)).filter(Submenu.menu_id == id).scalar_subquery()
    )
    dishes_count: Mapped[int] = column_property(
        select(func.coalesce(func.sum(Submenu.dishes_count), 0)).filter(Submenu.menu_id == id).scalar_subquery()
    )

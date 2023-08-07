import abc
import uuid

from sqlalchemy import BinaryExpression, and_

from app.models import Dish, Menu, Submenu


class SpecificationBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self) -> BinaryExpression:
        pass


class MenuSpecification(SpecificationBase):
    def __init__(self, menu_id: uuid.UUID):
        self.__menu_id = menu_id

    def execute(self) -> BinaryExpression:
        return Menu.id == self.__menu_id


class SubmenuListSpecification(SpecificationBase):
    def __init__(self, menu_id: uuid.UUID):
        self.__menu_id = menu_id

    def execute(self) -> BinaryExpression:
        return Submenu.menu_id == self.__menu_id


class SubmenuSpecification(SubmenuListSpecification):
    def __init__(self, menu_id: uuid.UUID, submenu_id: uuid.UUID):
        super().__init__(menu_id)

        self.__submenu_id = submenu_id

    def execute(self) -> BinaryExpression:
        return and_(super().execute(), Submenu.id == self.__submenu_id)


class DishListSpecification(SpecificationBase):
    def __init__(self, menu_id: uuid.UUID, submenu_id: uuid.UUID):
        self.__menu_id = menu_id
        self.__submenu_id = submenu_id

    def execute(self) -> BinaryExpression:
        return and_(Submenu.menu_id == self.__menu_id, Dish.submenu_id == self.__submenu_id)


class DishSpecification(DishListSpecification):
    def __init__(self, menu_id: uuid.UUID, submenu_id: uuid.UUID, dish_id: uuid.UUID):
        super().__init__(menu_id, submenu_id)

        self.__dish_id = dish_id

    def execute(self) -> BinaryExpression:
        return and_(super().execute(), Dish.id == self.__dish_id)

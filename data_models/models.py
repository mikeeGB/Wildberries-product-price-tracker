from typing import Literal
from collections import namedtuple

from pydantic import BaseModel


class Color(BaseModel):
    name: str


class Stock(BaseModel):
    qty: int


class Size(BaseModel):
    name: str
    origName: Literal["XS", "S", "M", "L", "XL", "XXL", "XXXL"] | str
    stocks: list[Stock] = []

    def quantity_available(self) -> int:
        return sum(stock.qty for stock in self.stocks)


SizeLeft = namedtuple("SizeLeft", ['RU', 'INTERNATIONAL', 'left'])


class Product(BaseModel):
    id: int
    brand: str
    colors: list[Color] = []
    name: str
    rating: int
    sizes: list[Size] = []
    salePriceU: int

    def get_available_sizes(self) -> list[SizeLeft]:
        return [
            SizeLeft(size.name, size.origName, size.quantity_available())
            for size in self.sizes if size.stocks
        ]


class WBCardData(BaseModel):
    products: list[Product]

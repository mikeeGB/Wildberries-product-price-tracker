from typing import Literal
from collections import namedtuple

from pydantic import BaseModel, field_validator, Field


class Color(BaseModel):
    name: str


class Stock(BaseModel):
    qty: int


class Size(BaseModel):
    name: str
    orig_name: Literal["XS", "S", "M", "L", "XL", "XXL", "XXXL"] | str = Field(alias='origName')
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
    sale_price: int = Field(alias='salePriceU')

    def get_available_sizes(self) -> list[SizeLeft]:
        return [
            SizeLeft(size.name, size.orig_name, size.quantity_available())
            for size in self.sizes if size.stocks
        ]

    @field_validator('sale_price')
    @classmethod
    def price_validate(cls, v):
        return round(v / 100, 2)


class WBCardData(BaseModel):
    products: list[Product]

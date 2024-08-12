from datetime import date
from typing import Union

from pydantic import BaseModel, Field, field_validator, EmailStr


class Address(BaseModel):
    province: str
    city: str


class User(BaseModel):
    # name: str = Field(pattern='^a')  # 正则表达式
    name: str
    password: str
    age: int = Field(default=20, gt=0, lt=100)  # 范围约束
    birthday: date
    email: EmailStr
    address: Address

    @field_validator('name')  # 限定校验字段
    def name_validator(cls, value):  # cls当前对象   value当前字段值
        assert value.isalpha(), 'name must be alpha'
        return value


class UserRes(BaseModel):
    name: str
    age: int = Field(default=20, gt=0, lt=100)  # 范围约束
    birthday: date
    email: EmailStr
    address: Address


class Item(BaseModel):
    name: str
    price: float = 10.2
    type: Union[str, None] = None


items = {
    'apple': {'name': 'apple', 'type': 'fruit'},
    'pen': {'name': 'pen', 'price': 10.2, 'type': 'tool'},
    'bike': {'name': 'bike', 'type': None}
}
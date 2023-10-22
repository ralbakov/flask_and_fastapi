'''
Задание
Необходимо создать базу данных для интернет-магазина. База данных должна состоять из трёх таблиц: товары, заказы и пользователи.
— Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
— Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
— Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
• Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
• Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.
• Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.

Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц.
Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API.
'''

from sqlalchemy import MetaData, Table, Column, Integer, Boolean, Float, Text, String, DateTime, ForeignKey, create_engine
from databases import Database
from fastapi import FastAPI
from pydantic import BaseModel, StrictInt, StrictStr, Field, EmailStr, StrictFloat, StrictBool
from random import choice, randint, uniform
from typing import List
from datetime import datetime


DATABASE_URL = 'sqlite:///./hw_les_06/sql_hw_6.db'

database = Database(DATABASE_URL)

metadata = MetaData()

goods = Table(
    'goods', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(50)),
    Column('description', Text),
    Column('price', Float(precision=2)),
)

orders = Table(
    'orders', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('goods_id', ForeignKey('goods.id')),
    Column('datatime', DateTime, default=datetime.now),
    Column('status', Boolean)
)

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(32)),
    Column('surname', String(32)),
    Column('email', String(100), unique=True),
    Column('password', String(50)),
)

engine = create_engine(
    DATABASE_URL, 
    connect_args={'check_same_thread': False}
)

metadata.create_all(engine)

app = FastAPI()

class UserIn(BaseModel):
    name: StrictStr = Field(max_length=32, title='Name')
    surname: StrictStr = Field(max_length=32, title='Surname')
    email: EmailStr = Field(max_length=100, title='Email')
    password: str = Field(max_length=50, title='Password')

class User(UserIn):
    id: int

class GoodsIn(BaseModel):
    description: StrictStr = Field(max_length=1000, title='Description')
    price: StrictFloat
    name: StrictStr = Field(max_length=50, title='Name')

class Product(GoodsIn):
    name: str

class OrderIn(BaseModel):
    user_id: StrictInt = Field(title='User_id')
    goods_id: StrictInt = Field(title='Product_id')
    datatime: datetime
    status: StrictBool = Field(title='Status')

class Order(OrderIn):
    id: int

@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

@app.get('/fake_users/{count}')
async def create_fake_users(count: int):
    for i in range(count):
        query = users.insert().values(
            name=f'name_{i}',
            surname=f'surname_{i}',
            email=f'mail{i}@mail.ru',
            password=f'{randint(100, 1000)}'
        )
        await database.execute(query)
    return {'msg': f'{count} fake users created'}

@app.get('/fake_goods/{count}')
async def create_fake_goods(count: int):
    for i in range(count):
        query = goods.insert().values(
            name=f'product_{i}',
            description=f'description_text_{i}',
            price=uniform(1, 1000),
        )
        await database.execute(query)
    return {'msg': f'{count} fake goods created'}

@app.get('/fake_orders/{count}')
async def create_fake_orders(count: int):
    for i in range(count):
        query = orders.insert().values(
            user_id=randint(1, count),
            goods_id=randint(1, count),
            datatime=datetime.now(),
            status=choice([True, False])
        )
        await database.execute(query)
    return {'msg': f'{count} fake orders created'}

@app.get('/users/', response_model=List[User])
async def read_users():
    query = users.select()
    our_user = await database.fetch_all(query)
    return our_user

@app.get('/goods/', response_model=List[Product])
async def read_goods():
    query = goods.select()
    our_goods = await database.fetch_all(query)
    return our_goods

@app.get('/orders/', response_model=List[Order])
async def read_orders():
    query = orders.select()
    our_orders = await database.fetch_all(query)
    return our_orders

@app.get('/users/{user_id}', response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    our_user = await database.fetch_one(query)
    return our_user

@app.get('/goods/{goods_id}', response_model=Product)
async def read_goods(goods_id: int):
    query = goods.select().where(goods.c.id == goods_id)
    our_goods = await database.fetch_one(query)
    return our_goods

@app.get('/orders/{orders_id}', response_model=Order)
async def read_orders(orders_id: int):
    query = orders.select().where(orders.c.id == orders_id)
    our_orders_id = await database.fetch_one(query)
    return our_orders_id

@app.post('/users/', response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(**user.model_dump())
    last_id = await database.execute(query)
    return {**user.model_dump(), "id": last_id}

@app.put('/goods/{prod_name}', response_model=Product)
async def update_goods(prod_name: str, new_prod: GoodsIn):
    query = goods.update().where(goods.c.name == prod_name).values(**new_prod.model_dump())
    await database.execute(query)
    return {**new_prod.model_dump(), "name": prod_name}

@app.delete('/orders/{order_status}')
async def del_orders(order_status: bool):
    query = orders.delete().where(orders.c.status == order_status)
    del_status = await database.execute(query)
    print(del_status)
    return {'msg': 'orders delete'}
import random
from typing import Any, List, Tuple
from datetime import datetime
from faker import Faker

import sqlalchemy
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from view import View


user = 'postgres'
password = 'Sqlpr0v0d0k'
host = 'localhost'
port = 5432
database = 'lab1'


Base = declarative_base()


def get_engine():
    return create_engine(url=f"postgresql://{user}:{password}@{host}:{port}/{database}")


def connect():
    try:
        _engine = get_engine()
        Base.metadata.create_all(_engine)
        print(f"Connection to the {host} for user {user} created successfully.")
        return sessionmaker(bind=_engine)()
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)


session = connect()


class Client(Base):
    __tablename__ = 'Client'
    client_id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name
        super(Client, self).__init__()


class Order(Base):
    __tablename__ = 'Order'
    order_id = Column(Integer, primary_key=True)
    date = Column(sqlalchemy.Time)
    category_id = Column(Integer, ForeignKey('Product_category.category_id'))
    client_id = Column(Integer, ForeignKey('Client.client_id'))
    store_id = Column(Integer, ForeignKey('Store.store_id'))

    category = relationship("ProductCategory", foreign_keys=[category_id])
    client = relationship("Client", foreign_keys=[client_id])
    store = relationship("Store", foreign_keys=[store_id])

    def __init__(self, date, category_id, client_id, store_id):
        self.date = date
        self.category_id = category_id
        self.client_id = client_id
        self.store_id = store_id
        super(Order, self).__init__()


class Product(Base):
    __tablename__ = 'Product'
    product_id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    category_id = Column(Integer, ForeignKey('Product_category.category_id'))

    category = relationship("ProductCategory", foreign_keys=[category_id])

    def __init__(self, name, price, category_id):
        self.name = name
        self.price = price
        self.category_id = category_id
        super(Product, self).__init__()


class ProductCategory(Base):
    __tablename__ = 'Product_category'
    category_id = Column(Integer, primary_key=True)
    name = Column(String)
    department_id = Column(Integer, ForeignKey('Store_department.department_id'))

    department = relationship("StoreDepartment", foreign_keys=[department_id])

    def __init__(self, name, department_id):
        self.name = name
        self.department_id = department_id
        super(ProductCategory, self).__init__()


class Store(Base):
    __tablename__ = 'Store'
    store_id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)

    def __init__(self, name, address):
        self.name = name
        self.address = address
        super(Store, self).__init__()


class StoreDepartment(Base):
    __tablename__ = 'Store_department'
    department_id = Column(Integer, primary_key=True)
    name = Column(String)
    store_id = Column(Integer, ForeignKey('Store.store_id'))

    store = relationship("Store", foreign_keys=[store_id])

    def __init__(self, name, store_id):
        self.name = name
        self.store_id = store_id
        super(StoreDepartment, self).__init__()


class OrderProduct(Base):
    __tablename__ = 'order_product'
    order_id = Column(Integer, ForeignKey('Order.order_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('Product.product_id'), primary_key=True)

    order = relationship("Order", foreign_keys=[order_id])
    product = relationship("Product", foreign_keys=[product_id])

    def __init__(self, order_id, product_id):
        self.order_id = order_id
        self.product_id = product_id
        super(OrderProduct, self).__init__()


def get_table_data(table) -> List[Tuple[Any]]:
    return [tuple(getattr(item, col.name) for col in item.__table__.columns)
            for item in session.query(table).all()]


def select_table(table_num, mode="w"):
    with open("table.txt", mode) as file:
        _view_obj = View()
        if table_num == 1:
            _view_obj.client_parser(get_table_data(Client), file)
        elif table_num == 2:
            _view_obj.order_parser(get_table_data(Order), file)
        elif table_num == 3:
            _view_obj.product_parser(get_table_data(Product), file)
        elif table_num == 4:
            _view_obj.product_category_parser(get_table_data(ProductCategory), file)
        elif table_num == 5:
            _view_obj.store_parser(get_table_data(Store), file)
        elif table_num == 6:
            _view_obj.store_department_parser(get_table_data(StoreDepartment), file)
        elif table_num == 7:
            _view_obj.order_product_parser(get_table_data(OrderProduct), file)


def clear_file(file_path: str) -> None:
    with open(file_path, "w"):
        pass


def select_all_tables():
    clear_file("table.txt")
    for table_num in range(1, 8):
        select_table(table_num, mode="a")


def insert_into_order(data):
    if data[0] == '-':
        data[0] = str(datetime.now().strftime("%H:%M:%S"))

    *data, _product_id = data
    session.add(Order(*data))
    session.commit()

    _order_id = session.query(Order).order_by(Order.order_id.desc()).first().order_id
    session.add(OrderProduct(_order_id, _product_id))


def insert_data_controller(table_num):
    _view_obj = View()
    if table_num == 1:
        data = _view_obj.input_client()
        session.add(Client(*data))
    elif table_num == 2:
        data = _view_obj.input_order()
        print("You can pass date column, Enter ' - '")
        insert_into_order(data)
    elif table_num == 3:
        data = _view_obj.input_product()
        session.add(Product(*data))
    elif table_num == 4:
        data = _view_obj.input_product_category()
        session.add(ProductCategory(*data))
    elif table_num == 5:
        data = _view_obj.input_store()
        session.add(Store(*data))
    elif table_num == 6:
        data = _view_obj.input_department()
        session.add(StoreDepartment(*data))
    elif table_num == 7:
        print("You cannot insert data into this table")
    session.commit()


def get_random_client_id():
    query = session.query(Client)
    row_count = int(query.count())
    return query.offset(int(row_count * random.random())).first().client_id


def insert_random_data_packet():
    _fake = Faker()

    session.add(Client(_fake.name()))

    _category_id = 18
    _client_id = get_random_client_id()
    _store_id = 1
    _product_id = 21
    insert_into_order(['-', _category_id, _client_id, _store_id, _product_id])

    _product_name = _fake.text().split()[0]
    _price = str(random.randint(100, 2000))
    session.add(Product(_product_name, _price, _category_id))

    _category_name = _fake.text().split()[0]
    _department_id = str(14)
    session.add(ProductCategory(_category_name, _department_id))

    _store_name = _fake.text().split()[0]
    _store_address = _fake.address()
    session.add(Store(_store_name, _store_address))

    _department_name = _fake.text().split()[0]
    session.add(StoreDepartment(_department_name, str(_store_id)))

    session.commit()


def get_active_column_names(row):
    columns = [col for col in row.__table__.columns.keys()]
    columns.pop(0)  # delete ID column
    return columns


def set_new_attr_values(row, data):
    columns = get_active_column_names(row)

    for column, d in zip(columns, data):
        if d != '-':
            row.__setattr__(column, d)


def update_client_table(data):
    client_id, *data = data
    _row = session.query(Client).filter(Client.client_id == int(client_id)).first()
    set_new_attr_values(_row, data)


def update_order_product_table(order_id, product_id):
    _row = session.query(OrderProduct).filter(OrderProduct.order_id == int(order_id)).first()
    set_new_attr_values(_row, [product_id])


def update_order_table(data):
    order_id, *data, product_id = data
    _row = session.query(Order).filter(Order.order_id == int(order_id)).first()
    set_new_attr_values(_row, data)

    if data[0] == '-':
        _row.date = datetime.now().strftime("%H:%M:%S")

    update_order_product_table(order_id, product_id)


def update_product_table(data):
    product_id, *data = data
    _row = session.query(Product).filter(Product.product_id == int(product_id)).first()
    set_new_attr_values(_row, data)


def update_product_category_table(data):
    category_id, *data = data
    _row = session.query(ProductCategory).filter(ProductCategory.category_id == int(category_id)).first()
    set_new_attr_values(_row, data)


def update_store_table(data):
    store_id, *data = data
    _row = session.query(Store).filter(Store.store_id == int(store_id)).first()
    set_new_attr_values(_row, data)


def update_store_department_table(data):
    department_id, *data = data
    _row = session.query(StoreDepartment).filter(StoreDepartment.department_id == int(department_id)).first()
    set_new_attr_values(_row, data)


def update_table_controller(table_num, data):
    if table_num == 1:
        update_client_table(data)
    elif table_num == 2:
        update_order_table(data)
    elif table_num == 3:
        update_product_table(data)
    elif table_num == 4:
        update_product_category_table(data)
    elif table_num == 5:
        update_store_table(data)
    elif table_num == 6:
        update_store_department_table(data)
    elif table_num == 7:
        update_order_product_table(*data)
    session.commit()


def get_range(id_range_to_delete):
    # begin == first value, end == second value (if it exists)
    # if there is no second value end == begin
    begin, end = id_range_to_delete[0], id_range_to_delete[-(len(id_range_to_delete) - 1)] + 1
    return range(begin, end)


def delete_rows(table, table_id, id_range):
    for _id in get_range(id_range):
        _row = session.query(table).filter(table_id == int(_id)).first()
        if _row:
            session.delete(_row)
            session.commit()


def delete_rows_controller(table_num, id_range):
    if table_num == 1:
        delete_rows(Client, Client.client_id, id_range)
    elif table_num == 2:
        delete_rows(Order, Order.order_id, id_range)
    elif table_num == 3:
        delete_rows(Product, Product.product_id, id_range)
    elif table_num == 4:
        delete_rows(ProductCategory, ProductCategory.category_id, id_range)
    elif table_num == 5:
        delete_rows(Store, Store.store_id, id_range)
    elif table_num == 6:
        delete_rows(StoreDepartment, StoreDepartment.departmentt_id, id_range)
    elif table_num == 7:
        print("You cannot delete data from this table")

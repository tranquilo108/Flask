from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float, func, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import List

from models import User, UserUpdate, UserCreate, Product, ProductCreate, ProductUpdate, Order, OrderCreate, OrderUpdate

Base = declarative_base()
engine = create_engine("sqlite:///market.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


class ProductDB(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)


class OrderDB(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    date = Column(DateTime, server_default=func.now())
    status = Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/users/", response_model=List[User])
def get_all_users():
    result = []
    db = SessionLocal()
    users = db.query(UserDB).all()
    db.close()
    if len(users) < 1:
        raise HTTPException(status_code=404, detail="Table User is empty")
    for user in users:
        result.append(User(**user.__dict__))
    return result


@app.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: int):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    db.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print(User(**user.__dict__))
    return User(**user.__dict__)


@app.post("/users/", response_model=User)
def create_user(user: UserCreate):
    db_user = UserDB(**user.dict())
    db = SessionLocal()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user


@app.put("/users/", response_model=UserUpdate)
def update_user(user_id: int, user_update: UserUpdate):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user is not None:
        for attr, value in user_update.dict(exclude_unset=True).items():
            setattr(user, attr, value)
        db.commit()
        db.close()
        return UserUpdate(**user_update.__dict__)
    db.close()
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/", response_model=User)
def delete_user(user_id: int):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user is None:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    db.close()
    return User(**user.__dict__)


@app.get("/products/", response_model=List[Product])
def get_all_products():
    result = []
    db = SessionLocal()
    products = db.query(ProductDB).all()
    db.close()
    if len(products) < 1:
        raise HTTPException(status_code=404, detail="Table Product is empty")
    for product in products:
        result.append(Product(**product.__dict__))
    return result


@app.get("/products/{product_id}", response_model=Product)
def get_product_by_id(product_id: int):
    db = SessionLocal()
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    db.close()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**product.__dict__)


@app.post("/products/", response_model=Product)
def create_product(product: ProductCreate):
    db_product = ProductDB(**product.dict())
    db = SessionLocal()
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    db.close()
    return db_product


@app.put("/products/", response_model=ProductUpdate)
def update_product(product_id: int, product_update: ProductUpdate):
    db = SessionLocal()
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if product is not None:
        for attr, value in product_update.dict(exclude_unset=True).items():
            setattr(product, attr, value)
        db.commit()
        db.close()
        return ProductUpdate(**product_update.__dict__)
    db.close()
    raise HTTPException(status_code=404, detail="Product not found")


@app.delete("/products/", response_model=Product)
def delete_product(product_id: int):
    db = SessionLocal()
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if product is None:
        db.close()
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    db.close()
    return Product(**product.__dict__)


@app.get("/orders/", response_model=List[Order])
def get_all_orders():
    result = []
    db = SessionLocal()
    orders = db.query(OrderDB).all()
    db.close()
    if len(orders) < 1:
        raise HTTPException(status_code=404, detail="Table Order is empty")
    for order in orders:
        print(order.status)
        result.append(Order(**order.__dict__))
    return result


@app.get("/orders/{order_id}", response_model=Order)
def get_order_by_id(order_id: int):
    db = SessionLocal()
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return Order(**order.__dict__)


@app.post("/orders/", response_model=Order)
def create_order(order: OrderCreate):
    db_order = OrderDB(**order.dict())
    db = SessionLocal()
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    db.close()
    return db_order


@app.put("/orders/", response_model=OrderUpdate)
def update_order(order_id: int, order_update: OrderUpdate):
    db = SessionLocal()
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if order is not None:
        for attr, value in order_update.dict(exclude_unset=True).items():
            setattr(order, attr, value)
        db.commit()
        db.close()
        return OrderUpdate(**order_update.__dict__)
    db.close()
    raise HTTPException(status_code=404, detail="Order not found")


@app.delete("/orders/", response_model=Order)
def delete_order(order_id: int):
    db = SessionLocal()
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if order is None:
        db.close()
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    db.close()
    return Order(**order.__dict__)

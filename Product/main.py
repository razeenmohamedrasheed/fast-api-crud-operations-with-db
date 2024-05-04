from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from . import schemas
from . import models
from .db import engine,SessionLocal

app = FastAPI()

models.Base.metadata.create_all(engine)

def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/products')
def addProducts(request:schemas.Product,db:Session = Depends(getDB)):
    new_product = models.Product(name=request.name,
                                 description=request.description,
                                 price=request.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request

@app.get('/products')
def ListProducts(db:Session = Depends(getDB)):
    products = db.query(models.Product).all()
    return {
        "message":"Success",
        "data":products
    }


@app.get('/products/{id}')
def ListProducts(id,db:Session = Depends(getDB)):
    product = db.query(models.Product).filter(models.Product.id== id).first()
    return {
        "message":"Success",
        "data":product
    }


@app.delete('/products/{id}')
def DeleteProducts(id,db:Session = Depends(getDB)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    products = db.query(models.Product).all()
    return {
        "message":"Success",
        "data":products
    }

@app.put('/products/{id}')
def UpdateProducts(id,request:schemas.Product,db:Session = Depends(getDB)):
    product = db.query(models.Product).filter(models.Product.id== id).first()
    if not product:
        return "product not found"
    product.name = request.name
    product.description = request.description
    product.price = request.price
    
    db.commit()
    db.refresh(product)
    return product

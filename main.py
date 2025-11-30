from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import lib  # Your legacy library

from database import get_db, create_tables
from models import Product, Category
from pydantic import BaseModel

app = FastAPI()


@app.on_event("startup")
def startup_event():
    create_tables()

class OrderRequest(BaseModel):
    product_id: int
    quantity: int

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    category_id: int
    category_name: str
    
    class Config:
        orm_mode = True

@app.get("/api/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product, Category.name.label('category_name'))\
        .join(Category, Product.category_id == Category.id)\
        .all()
    
    return [
        ProductResponse(
            id=product.id,
            name=product.name,
            price=product.price,
            stock=product.stock,
            category_id=product.category_id,
            category_name=category_name
        )
        for product, category_name in products
    ]

@app.post("/api/order")
def create_order(order: OrderRequest, db: Session = Depends(get_db)):
    # Get product from database
    product = db.query(Product).filter(Product.id == order.product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.stock < order.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    # Use the legacy library to calculate price
    total_price = lib.calculate_price(product.price, order.quantity)
    
    # Update stock
    product.stock -= order.quantity
    db.commit()
    
    return {
        "product_id": product.id,
        "product_name": product.name,
        "quantity": order.quantity,
        "unit_price": product.price,
        "total_price": total_price,
        "remaining_stock": product.stock
    }

@app.get("/")
def read_root():
    return {"message": "Inventory API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

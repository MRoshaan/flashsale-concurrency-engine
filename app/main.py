# app/main.py the broken version
'''from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import time
from . import models, database, schemas # <--- Added schemas import

app = FastAPI()

# Dependency
get_db = database.get_db

@app.get("/")
def read_root():
    return {"message": "FlashSale API is ready to crash!"}

# --- NEW: Helper endpoint to create a user (so you don't have to use SQL) ---
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- NEW: Helper endpoint to create a product ---
@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(
        product_Name=product.product_Name, # Matches your specific column
        price=product.price,
        stock_quantity=product.stock_quantity
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# --- THE BROKEN BUY ENDPOINT ---
# (Logic remains the same, but now it's part of the complete picture)
@app.post("/buy/{product_id}")
def buy_product(product_id: int, db: Session = Depends(get_db)):
    # 1. Fetch Product
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # 2. Check Stock
    if product.stock_quantity <= 0:
        return {"message": "Out of stock!", "success": False}

    # ---------------------------------------------------------
    # THE DANGER ZONE (0.2s Delay)
    time.sleep(0.2) 
    # ---------------------------------------------------------

    # 3. Decrease Stock
    product.stock_quantity = product.stock_quantity - 1
    
    # 4. Create Order
    order = models.Order(
        user_id=1, 
        product_id=product_id, 
        status="COMPLETED"
    )
    db.add(order)
    
    # 5. Commit
    db.commit()
    db.refresh(product)
    
    return {
        "message": f"Sold! Stock remaining: {product.stock_quantity}", 
        "success": True
    }'''
# app/main.py the fixed version
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import time
from . import models, database, schemas

app = FastAPI()

get_db = database.get_db

@app.post("/buy/{product_id}")
def buy_product(product_id: int, db: Session = Depends(get_db)):
    
    # --- START TRANSACTION ---
    # We don't need to manually write "BEGIN", SQLAlchemy handles it.

    # 1. FETCH WITH LOCK (The Fix)
    # with_for_update() locks the row in MySQL. 
    # User 2 has to WAIT here until User 1 finishes.
    product = db.query(models.Product).filter(models.Product.id == product_id).with_for_update().first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # 2. CHECK STOCK
    if product.stock_quantity <= 0:
        return {"message": "Out of stock!", "success": False}

    # ---------------------------------------------------------
    # SIMULATING LATENCY
    # Even with this sleep, the lock holds! 
    # No one else can enter the critical section.
    time.sleep(0.2) 
    # ---------------------------------------------------------

    # 3. DECREASE STOCK
    product.stock_quantity -= 1
    
    # 4. CREATE ORDER
    order = models.Order(
        user_id=1, 
        product_id=product_id, 
        status="COMPLETED"
    )
    db.add(order)
    
    # 5. COMMIT (Releases the Lock)
    db.commit()
    db.refresh(product)
    
    return {
        "message": f"Sold! Stock remaining: {product.stock_quantity}", 
        "success": True
    }
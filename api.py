from fastapi import FastAPI
from models.foods import FoodItem
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

items_db = []

class FoodItem(BaseModel):
    name: str
    food_id: Optional[int]
    food_desc: Optional[str]
    has_kilo_price: Optional[bool]
    has_piece_price: Optional[bool]
    price_per_kilo: Optional[float]
    deleted_price_per_kilo: Optional[float]
    deleted_main_price: Optional[float]
    main_price: float
    food_photo: Optional[str]

@app.get("/")
def read_root():
    return {"food": "{FoodItem}"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = "name"):
    return {"item_id": item_id, "q": q}

# Endpoint to create a new item and store it in the items_db
@app.post("/items/")
async def create_item(item: FoodItem):
    items_db.append(item)
    return item

# Endpoint to retrieve all items
@app.get("/items/", response_model=List[FoodItem])
async def get_all_items():
    return items_db




# uvicorn api:app --reload

from fastapi import FastAPI
from models.foods import FoodItem

app = FastAPI()

@app.get("/")
def read_root():
    return {"food": "{FoodItem}"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = "hell"):
    return {"item_id": item_id, "q": q}


# uvicorn api:app --reload

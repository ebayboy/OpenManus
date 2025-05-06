from typing import Union

from fastapi import Body, FastAPI, Header, Query
from pydantic import BaseModel

app = FastAPI()

# https://www.runoob.com/fastapi/fastapi-pydantic.html


# BaseModel 模型序列化
class Item(BaseModel):
    name: str
    price: float


# root get
@app.get("/")
async def read_root(user_agent: str = Header(...)):
    print(f"read_root ...")
    return {"User-Agent": user_agent}


# items post
@app.post("/items/")
async def create_item(
    item: Item,
    user_agent: str = Header(...),
    item_id: str = Query(...),
):
    print(f"create_item...")
    print(f"item:{item}  user_agent:{user_agent} uuid:{item_id}")
    return {"item": item, "user_agent": user_agent, "item_id": item_id}


# items get
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    print("read_item...")
    return {"item_id": item_id, "q": q}

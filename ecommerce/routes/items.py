from microframe.routing import Router



router = Router(
    prefix="/items",
    tags=["items", "ecommerce"],

)

fake_items_db = ["item1", "item2", "item3"]

@router.put("/{item_id}", summary="Update an item by ID", response_model=str)
def update_item(item_id: int, item_name: str):
    fake_items_db[item_id] = item_name
    return item_name

@router.get("/", summary="Get all items", response_model=list[str])
def get_items():
    return fake_items_db

@router.get("/{item_id}", summary="Get an item by ID", response_model=str)
def get_item(item_id: int):
    return fake_items_db[item_id]

@router.post("/", summary="Create a new item", response_model=str)
def create_item(item_name: str):
    fake_items_db.append(item_name)
    return item_name

@router.delete("/{item_id}", summary="Delete an item by ID", response_model=str)
def delete_item(item_id: int):
    return fake_items_db.pop(item_id)

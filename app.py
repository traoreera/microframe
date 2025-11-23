from microframe import Application
from microframe.core.exceptions import NotFoundException
from pydantic import BaseModel
app = Application()


class User(BaseModel):
    id: int 

@app.get("/users/{user_id}")
async def get_user(user_id: User):
    print(user_id, type(user_id))
    if int(user_id.id) == 1:
        return  NotFoundException(f"User not found").to_dict()
    return {"user_id": user_id}
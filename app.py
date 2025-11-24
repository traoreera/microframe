from microframe import Application, Router



app = Application()
        
        # Main API router
api_router = Router(prefix="/api")
        

users_router = Router(prefix="/users", tags=["Users"])
posts_router = Router(prefix="/posts", tags=["Posts"])


@users_router.get("/")
async def list_users():
    return {"users": []}

@users_router.get("/{user_id}")
async def get_user(user_id: str):
    return {"user_id": user_id}

        # Posts sub-router


@posts_router.get("/")
async def list_posts():
    return {"posts": []}

        # Include sub-routers
api_router.include_router(users_router)
api_router.include_router(posts_router)


app.include_router(api_router, "/api")
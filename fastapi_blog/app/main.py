from fastapi import FastAPI
from app.modules.users.router import router as user_router
from app.modules.auth.router import router as auth_router
from app.modules.posts.router import router as posts_router

app = FastAPI(title="Professional Blog API")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(posts_router)

@app.get("/")
def root():
    return {"message": "Health check"}
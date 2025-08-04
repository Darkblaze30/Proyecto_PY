from fastapi import FastAPI
# from app.auth.controller import router as auth_router
from app.routes.example_route import router as example_router
from app.utils.database import create_db_and_tables

app = FastAPI()

# app.include_router(auth_router, prefix="/api/auth")
app.include_router(example_router, prefix="/api")

@app.on_event('startup')
def on_startup():
    create_db_and_tables()


@app.get("/")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)

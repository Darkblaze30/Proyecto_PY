from fastapi import FastAPI
# from app.auth.controller import router as auth_router
from app.utils.database import create_db_and_tables
from app.routes.auth_route import auth_router
from app.routes.user_route import user_router
from app.routes.room_route import room_router
from app.routes.reservation_route import reservation_router


app = FastAPI()


app.include_router(auth_router)

app.include_router(user_router)

app.include_router(room_router)

app.include_router(reservation_router)


@app.get("/")
def health_check():
    return {"status": "ok"}

@app.on_event('startup')
def on_startup():
    create_db_and_tables()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)


from fastapi import FastAPI, status
from app.routes.user_routes import user_router
from app.routes.task_router import task_router
from app.database.database import Base, engine
from app.models import user, task


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get(
        "/", 
        status_code=status.HTTP_200_OK)
def root():
    return {"Message": "Hello World!!!"}



app.include_router(user_router)
app.include_router(task_router)
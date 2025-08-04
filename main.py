from fastapi import FastAPI, status
from fastapi_mcp import FastApiMCP
from app.routes.user_routes import user_router
from app.routes.evento_routes import router as evento_router
from app.database.database import Base, engine
from app.models import user, task, evento


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(evento_router)


mcp = FastApiMCP(
    app,
    description="Task manager api mcp server."
)

mcp.mount()
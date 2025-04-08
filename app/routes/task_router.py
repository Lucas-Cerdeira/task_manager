from fastapi import APIRouter
from app.schemas.task import TaskBase

task_router = APIRouter()


@task_router.get("/task/", tags=["Tasks"])
def get_task():
    return [{"nome":"Lavar Louça"},
            {"descricao":"Lavar toda a louça da pia."},
            {"completed":False},
            {"user_id":1}
    ]

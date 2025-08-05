from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.schemas.tool_registry import Tool, FieldSchema, SchemaDefinition
from typing import List

router = APIRouter(prefix="/tool-registry", tags=["Tool Registry"])

def get_tools() -> List[Tool]:
    """Retorna a lista de todas as ferramentas disponíveis na API"""
    tools = [
        Tool(
            name="create_task",
            description="Cria uma nova tarefa para um usuário",
            url="/users/{user_id}/create_task/",
            method="POST",
            schema=SchemaDefinition(
                input={
                    "nome": FieldSchema(type="string", description="Nome da tarefa"),
                    "descricao": FieldSchema(type="string", description="Descrição detalhada da tarefa"),
                    "completed": FieldSchema(type="boolean", description="Status de conclusão da tarefa"),
                    "data_entrega": FieldSchema(type="string", description="Data de entrega (formato ISO)", required=False),
                    "diaria": FieldSchema(type="boolean", description="Indica se é uma tarefa diária")
                },
                output={
                    "id": FieldSchema(type="integer", description="ID da tarefa criada"),
                    "nome": FieldSchema(type="string", description="Nome da tarefa"),
                    "descricao": FieldSchema(type="string", description="Descrição da tarefa"),
                    "completed": FieldSchema(type="boolean", description="Status de conclusão"),
                    "data_criacao": FieldSchema(type="string", description="Data de criação da tarefa"),
                    "data_entrega": FieldSchema(type="string", description="Data de entrega", required=False),
                    "diaria": FieldSchema(type="boolean", description="Indica se é uma tarefa diária"),
                    "user_id": FieldSchema(type="integer", description="ID do usuário proprietário")
                }
            )
        ),
        Tool(
            name="get_task",
            description="Retorna os detalhes de uma tarefa específica",
            url="/users/{user_id}/tasks/{task_id}/",
            method="GET",
            schema=SchemaDefinition(
                input={
                    "user_id": FieldSchema(type="integer", description="ID do usuário"),
                    "task_id": FieldSchema(type="integer", description="ID da tarefa")
                },
                output={
                    "id": FieldSchema(type="integer", description="ID da tarefa"),
                    "nome": FieldSchema(type="string", description="Nome da tarefa"),
                    "descricao": FieldSchema(type="string", description="Descrição da tarefa"),
                    "completed": FieldSchema(type="boolean", description="Status de conclusão"),
                    "data_criacao": FieldSchema(type="string", description="Data de criação da tarefa"),
                    "data_entrega": FieldSchema(type="string", description="Data de entrega", required=False),
                    "diaria": FieldSchema(type="boolean", description="Indica se é uma tarefa diária"),
                    "user_id": FieldSchema(type="integer", description="ID do usuário proprietário")
                }
            )
        ),
        Tool(
            name="update_task",
            description="Atualiza os detalhes de uma tarefa existente",
            url="/users/{user_id}/tasks/{task_id}/",
            method="PUT",
            schema=SchemaDefinition(
                input={
                    "nome": FieldSchema(type="string", description="Novo nome da tarefa", required=False),
                    "descricao": FieldSchema(type="string", description="Nova descrição da tarefa", required=False),
                    "completed": FieldSchema(type="boolean", description="Novo status de conclusão", required=False),
                    "data_entrega": FieldSchema(type="string", description="Nova data de entrega", required=False),
                    "diaria": FieldSchema(type="boolean", description="Novo status de tarefa diária", required=False)
                },
                output={
                    "id": FieldSchema(type="integer", description="ID da tarefa"),
                    "nome": FieldSchema(type="string", description="Nome atualizado da tarefa"),
                    "descricao": FieldSchema(type="string", description="Descrição atualizada"),
                    "completed": FieldSchema(type="boolean", description="Status de conclusão atualizado"),
                    "data_criacao": FieldSchema(type="string", description="Data de criação original"),
                    "data_entrega": FieldSchema(type="string", description="Data de entrega atualizada", required=False),
                    "diaria": FieldSchema(type="boolean", description="Status atualizado de tarefa diária"),
                    "user_id": FieldSchema(type="integer", description="ID do usuário proprietário")
                }
            )
        ),
        Tool(
            name="delete_task",
            description="Remove uma tarefa específica",
            url="/users/{user_id}/tasks/{task_id}/",
            method="DELETE",
            schema=SchemaDefinition(
                input={
                    "user_id": FieldSchema(type="integer", description="ID do usuário"),
                    "task_id": FieldSchema(type="integer", description="ID da tarefa a ser deletada")
                },
                output={
                    "message": FieldSchema(type="string", description="Mensagem de confirmação")
                }
            )
        )
    ]
    return tools

@router.get("/", response_model=List[Tool])
async def tool_registry():
    """
    Retorna uma lista de todas as ferramentas disponíveis na API com suas descrições,
    endpoints e schemas.
    """
    tools = get_tools()
    return JSONResponse(content=[tool.model_dump() for tool in tools])

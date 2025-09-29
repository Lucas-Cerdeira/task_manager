import pytest
from fastapi import status
from httpx import AsyncClient
from unittest.mock import patch
from app.schemas.tool_registry import Tool, FieldSchema, SchemaDefinition

# Mock data para testes
MOCK_TOOLS = [
    Tool(
        name="create_task",
        description="Cria uma nova tarefa",
        url="/users/{user_id}/create_task/",
        method="POST",
        schema=SchemaDefinition(
            input={
                "nome": FieldSchema(type="string", description="Nome da tarefa"),
                "descricao": FieldSchema(type="string", description="Descrição da tarefa")
            },
            output={
                "id": FieldSchema(type="integer", description="ID da tarefa criada"),
                "nome": FieldSchema(type="string", description="Nome da tarefa")
            }
        )
    ),
    Tool(
        name="get_task",
        description="Obtém detalhes de uma tarefa",
        url="/users/{user_id}/tasks/{task_id}/",
        method="GET",
        schema=SchemaDefinition(
            input={},
            output={
                "id": FieldSchema(type="integer", description="ID da tarefa"),
                "nome": FieldSchema(type="string", description="Nome da tarefa")
            }
        )
    )
]

@pytest.mark.asyncio
async def test_tool_registry_status(client, base_url):
    """Testa se o endpoint retorna status 200 OK"""
    async with AsyncClient(base_url=base_url) as ac:
        with patch('app.routes.tool_registry.get_tools', return_value=MOCK_TOOLS):
            response = await ac.get("/tool-registry/")
            assert response.status_code == status.HTTP_200_OK, "O endpoint deve retornar status 200"

@pytest.mark.asyncio
async def test_tool_registry_response_structure(client, base_url):
    """Testa se a resposta tem a estrutura correta"""
    async with AsyncClient(base_url=base_url) as ac:
        with patch('app.routes.tool_registry.get_tools', return_value=MOCK_TOOLS):
            response = await ac.get("/tool-registry/")
            data = response.json()
            
            assert isinstance(data, list), "A resposta deve ser uma lista"
            assert len(data) > 0, "A lista não deve estar vazia"

@pytest.mark.asyncio
async def test_tool_registry_tool_structure(client, base_url):
    """Testa se cada ferramenta tem todos os campos obrigatórios"""
    async with AsyncClient(base_url=base_url) as ac:
        with patch('app.routes.tool_registry.get_tools', return_value=MOCK_TOOLS):
            response = await ac.get("/tool-registry/")
            tools = response.json()
            
            for tool in tools:
                # Verifica campos obrigatórios
                assert all(key in tool for key in ["name", "description", "url", "method", "schema"]), \
                    f"Ferramenta {tool.get('name', 'unknown')} não tem todos os campos obrigatórios"
                
                # Verifica estrutura do schema
                assert "input" in tool["schema"], f"Schema da ferramenta {tool['name']} deve ter campo 'input'"
                assert "output" in tool["schema"], f"Schema da ferramenta {tool['name']} deve ter campo 'output'"

@pytest.mark.asyncio
async def test_tool_registry_method_validation(client, base_url):
    """Testa se os métodos HTTP são válidos"""
    async with AsyncClient(base_url=base_url) as ac:
        with patch('app.routes.tool_registry.get_tools', return_value=MOCK_TOOLS):
            response = await ac.get("/tool-registry/")
            tools = response.json()
            
            valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
            for tool in tools:
                assert tool["method"] in valid_methods, \
                    f"Método HTTP '{tool['method']}' da ferramenta '{tool['name']}' deve ser válido"

@pytest.mark.asyncio
async def test_tool_registry_url_format(client, base_url):
    """Testa se as URLs das ferramentas estão no formato correto"""
    async with AsyncClient(base_url=base_url) as ac:
        with patch('app.routes.tool_registry.get_tools', return_value=MOCK_TOOLS):
            response = await ac.get("/tool-registry/")
            tools = response.json()
            
            for tool in tools:
                assert tool["url"].startswith("/"), \
                    f"URL da ferramenta '{tool['name']}' deve começar com '/'"
                assert len(tool["url"]) > 1, \
                    f"URL da ferramenta '{tool['name']}' deve ter mais de um caractere"

@pytest.mark.asyncio
async def test_tool_registry_description_quality(client, base_url):
    """Testa a qualidade das descrições das ferramentas"""
    async with AsyncClient(base_url=base_url) as ac:
        with patch('app.routes.tool_registry.get_tools', return_value=MOCK_TOOLS):
            response = await ac.get("/tool-registry/")
            tools = response.json()
            
            for tool in tools:
                description = tool["description"]
                assert len(description) >= 10, \
                    f"Descrição da ferramenta '{tool['name']}' deve ter pelo menos 10 caracteres"
                assert description[0].isupper(), \
                    f"Descrição da ferramenta '{tool['name']}' deve começar com letra maiúscula"

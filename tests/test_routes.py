import pytest
from app.schemas.user import UserCreate
from app.schemas.task import TaskCreate
from app.schemas.evento import EventoCreate
from app.db_services.user import UserDbServices
from app.db_services.task import TaskDbServices
from app.db_services.evento import EventoDbServices
from datetime import datetime


def test_create_user(client):
    user_data = {
        "nome": "Teste",
        "sobrenome": "User",
        "email": "testeuser@example.com",
        "senha_hash": "senha123"
    }
    response = client.post("/users/create_user/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["nome"] == user_data["nome"]


def test_get_user_by_email(client):
    user_data = {
        "nome": "Email",
        "sobrenome": "Test",
        "email": "emailtest@example.com",
        "senha_hash": "senha123"
    }
    client.post("/users/create_user/", json=user_data)
    response = client.get(f"/users/email/?email={user_data['email']}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]


def test_get_user_by_id(client, db_session):
    user_data = {
        "nome": "Id",
        "sobrenome": "Test",
        "email": "idtest@example.com",
        "senha_hash": "senha123"
    }
    response = UserDbServices.create_user(user=UserCreate(**user_data), db=db_session)
    user_id = response.id

    response = client.get(f"/users/{user_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]


def test_update_user(client, db_session):
    user_data = {
        "nome": "Update",
        "sobrenome": "Test",
        "email": "updatetest@example.com",
        "senha_hash": "senha123"
    }

    response = UserDbServices.create_user(user=UserCreate(**user_data), db=db_session)
    user_id = response.id
    
    update_data = {"nome": "NovoNome", "sobrenome": "NovoSobrenome", "email": "novoemail@example.com"}
    response = client.put(f"/users/update/{user_id}/", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "NovoNome"


def test_create_task_for_user(client, db_session):
    user_data = {
        "nome": "Task",
        "sobrenome": "User",
        "email": "taskuser@example.com",
        "senha_hash": "senha123"
    }
    response = UserDbServices.create_user(user=UserCreate(**user_data), db=db_session)
    user_id = response.id

    task_data = {
        "nome": "Tarefa Teste",
        "descricao": "Descrição da tarefa",
        "completed": False,
        "data_entrega": None,
        "diaria": False
    }
    response = client.post(f"/users/{user_id}/create_task/", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == task_data["nome"]


def test_get_tasks_by_user_id(client, db_session):
    user_data = {
        "nome": "TaskList",
        "sobrenome": "User",
        "email": "tasklistuser@example.com",
        "senha_hash": "senha123"
    }

    response = UserDbServices.create_user(user=UserCreate(**user_data), db=db_session)
    user_id = response.id
    
    task_data = {
        "nome": "Tarefa Lista",
        "descricao": "Descrição da tarefa lista",
        "completed": False,
        "data_entrega": None,
        "diaria": False
    }
    
    client.post(f"/users/{user_id}/create_task/", json=task_data)
    response = client.get(f"/users/{user_id}/tasks/")
    
    assert response.status_code == 200
    data = response.json()


def test_delete_task_for_user(client, db_session):
    user_data = {
        "nome": "DeleteTask",
        "sobrenome": "User",
        "email": "deletetaskuser@example.com",
        "senha_hash": "senha123"
    }

    response = UserDbServices.create_user(user=UserCreate(**user_data), db=db_session)
    user_id = response.id

    task_data = {
        "nome": "Tarefa Deletar",
        "descricao": "Descrição da tarefa deletar",
        "completed": False,
        "data_entrega": None,
        "diaria": False
    }

    response = TaskDbServices.create_task(user_id=user_id, task=TaskCreate(**task_data), db=db_session)
    task_id = response.id

    response = client.delete(f"/users/{user_id}/tasks/{task_id}/")
    assert response.status_code in [200, 204]


def test_create_evento_for_user(client, db_session):
    user_data = {
        "nome": "Evento",
        "sobrenome": "User",
        "email": "eventouser@example.com",
        "senha_hash": "senha123"
    }
    response = UserDbServices.create_user(user=UserCreate(**user_data), db=db_session)
    user_id = response.id

    evento_data = {
        "titulo": "Reunião de Projeto",
        "descricao": "Discussão sobre novos recursos",
        "local": "Sala de Conferência",
        "data_evento": datetime.utcnow().isoformat()
    }
    response = client.post(f"/users/{user_id}/create_evento/", json=evento_data)
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == evento_data["titulo"]
    assert data["local"] == evento_data["local"]


def test_get_eventos_by_user_id(client, db_session):
    user_data = {
        "nome": "EventoList",
        "sobrenome": "User",
        "email": "eventolistuser@example.com",
        "senha_hash": "senha123"
    }
    response = UserDbServices.create_user(user=UserCreate(**user_data), db=db_session)
    user_id = response.id

    evento_data = {
        "titulo": "Workshop de Python",
        "descricao": "Introdução ao FastAPI",
        "local": "Auditório Principal",
        "data_evento": datetime.utcnow().isoformat()
    }
    
    client.post(f"/users/{user_id}/create_evento/", json=evento_data)
    response = client.get(f"/users/{user_id}/eventos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["titulo"] == evento_data["titulo"]


def test_update_evento(client, db_session):
    user_data = {
        "nome": "EventoUpdate",
        "sobrenome": "User",
        "email": "eventoupdate@example.com",
        "senha_hash": "senha123"
    }
    response = UserDbServices.create_user(user=UserCreate(**user_data), db=db_session)
    user_id = response.id

    evento_data = {
        "titulo": "Evento Original",
        "descricao": "Descrição Original",
        "local": "Local Original",
        "data_evento": datetime.utcnow().isoformat()
    }
    
    response = client.post(f"/users/{user_id}/create_evento/", json=evento_data)
    evento_id = response.json()["id"]

    update_data = {
        "titulo": "Evento Atualizado",
        "local": "Novo Local"
    }
    
    response = client.put(f"/users/{user_id}/eventos/{evento_id}/", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == update_data["titulo"]
    assert data["local"] == update_data["local"]
    assert data["descricao"] == evento_data["descricao"]  # Campo não atualizado deve manter valor original


def test_delete_evento(client, db_session):
    user_data = {
        "nome": "EventoDelete",
        "sobrenome": "User",
        "email": "eventodelete@example.com",
        "senha_hash": "senha123"
    }
    response = UserDbServices.create_user(user=UserCreate(**user_data), db=db_session)
    user_id = response.id

    evento_data = {
        "titulo": "Evento para Deletar",
        "descricao": "Este evento será deletado",
        "local": "Local Temporário",
        "data_evento": datetime.utcnow().isoformat()
    }
    
    evento = EventoCreate(**evento_data)
    response = EventoDbServices.create_evento(db=db_session, evento=evento, user_id=user_id)
    evento_id = response.id

    response = client.delete(f"/users/{user_id}/eventos/{evento_id}/")
    assert response.status_code in [200, 204]

    # Verifica se o evento foi realmente deletado
    response = client.get(f"/users/{user_id}/eventos/")
    assert response.status_code == 200
    data = response.json()
    assert not any(evento["id"] == evento_id for evento in data)

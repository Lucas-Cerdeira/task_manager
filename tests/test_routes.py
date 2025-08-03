import pytest
from app.schemas.user import UserCreate
from app.schemas.task import TaskCreate
from app.db_services.user import UserDbServices
from app.db_services.task import TaskDbServices


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

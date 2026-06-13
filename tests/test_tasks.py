from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "La API de tareas funciona correctamente"


def test_create_task():
    response = client.post("/tasks", json={"title": "Estudiar Docker"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Estudiar Docker"
    assert data["completed"] is False


def test_list_tasks():
    client.post("/tasks", json={"title": "Hacer pruebas"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_task():
    create_response = client.post("/tasks", json={"title": "Eliminar esta tarea"})
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Tarea eliminada correctamente"


def test_get_task_by_id():
    create_response = client.post("/tasks", json={"title": "Buscar tarea por ID"})
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Buscar tarea por ID"


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["message"] == "La aplicacion esta activa"

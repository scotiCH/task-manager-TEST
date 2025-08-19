from getgauge.python import step, data_store
from fastapi.testclient import TestClient
import json
from uuid import UUID

from app.main import app
from app.models import Status

client = TestClient(app)

@step("Создать задачу с названием <title> и описанием <description>")
def create_task(title: str, description: str):
    response = client.post(
        "/tasks/",
        json={"title": title, "description": description}
    )
    assert response.status_code == 201
    task_data = response.json()
    data_store.scenario["task_id"] = task_data["id"]
    data_store.scenario["task"] = task_data  # Сохраняем для последующих проверок

@step("Получить задачу по ID и проверить название <title> описание <description> статус <status>")
def get_and_check_task(title: str, description: str, status: str):
    task_id = data_store.scenario["task_id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    task = response.json()
    assert task["title"] == title
    assert task["description"] == description
    assert task["status"] == status

@step("Получить все задачи и проверить, что количество равно <count>")
def get_tasks_and_check_count(count: int):
    response = client.get("/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == count

@step("Обновить задачу с новым названием <title> новым описанием <description> новым статусом <status>")
def update_task(title: str, description: str, status: str):
    task_id = data_store.scenario["task_id"]
    response = client.put(
        f"/tasks/{task_id}",
        json={"title": title, "description": description, "status": status}
    )
    assert response.status_code == 200

@step("Удалить задачу по ID")
def delete_task():
    task_id = data_store.scenario["task_id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

@step("Получить задачу по ID и ожидать, что не найдено")
def get_task_expect_not_found():
    task_id = data_store.scenario.get("task_id", "00000000-0000-0000-0000-000000000000")  # Используем недействительный, если не задан
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404

@step("Получить несуществующую задачу и ожидать, что не найдено")
def get_non_existent():
    response = client.get("/tasks/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404

@step("Обновить несуществующую задачу и ожидать, что не найдено")
def update_non_existent():
    response = client.put(
        "/tasks/00000000-0000-0000-0000-000000000000",
        json={"title": "Invalid"}
    )
    assert response.status_code == 404

@step("Удалить несуществующую задачу и ожидать, что не найдено")
def delete_non_existent():
    response = client.delete("/tasks/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
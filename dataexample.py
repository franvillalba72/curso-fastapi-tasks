from schemes import StatusType

task_with_ORM = {
    "id": 1,
    "name": "Tarea de prueba 1",
    "description": "Tarea de prueba 1",
    "status": StatusType.PENDING,
    "category_id": 1,
    "user_id": 1
}

tasks_with_ORM = {
    "normal1": {
        "id": 1,
        "name": "Tarea de prueba 1",
        "description": "Tarea de prueba 1",
        "status": StatusType.PENDING,
        "category": 1,
        "user": 1
    },
    "normal2": {
        "id": 2,
        "name": "Tarea de prueba 2",
        "description": "Tarea de prueba 2",
        "status": StatusType.PENDING,
        "category": 1,
        "user": 1
    },
    "normal3": {
        "id": 3,
        "name": "Tarea de prueba 3",
        "description": "Tarea de prueba 3",
        "status": StatusType.PENDING,
        "category": 1,
        "user": 1
    },
}

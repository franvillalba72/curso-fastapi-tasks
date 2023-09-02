from fastapi import APIRouter, status, HTTPException
from models import Task

router = APIRouter()

task_list = []


@router.get('/', status_code=status.HTTP_200_OK)
def get():
    return {'tasks': task_list}


@router.post('/', status_code=status.HTTP_201_CREATED)
def add(task: Task):
    # Verificamos que la tarea no existe
    if task in task_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Task {task.name} already exists"
        )
        return

    task_list.append(task)
    return {'tasks': task_list}


@router.put('/', status_code=status.HTTP_200_OK)
def update(index: int, task: Task):
    # Verificamos que el índice existe
    if len(task_list) <= index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task ID doesn't exists"
        )

    task_list[index] = task
    return {'tasks': task_list}


@router.delete('/', status_code=status.HTTP_200_OK)
def delete(index: int):
    # Verificamos que el índice existe
    if len(task_list) <= index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task ID doesn't exists"
        )

    del task_list[index]
    return {'tasks': task_list}

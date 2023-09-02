from fastapi import APIRouter, Body
from models import Task

router = APIRouter()

task_list = []


@router.get('/')
def get():
    return {'tasks': task_list}


@router.post('/')
def add(task: Task):
    task_list.append(task)
    # task_list.append({
    #     "task": task,
    #     "status": StatusType.PENDING
    # })
    return {'tasks': task_list}


@router.put('/')
def update(index: int, task: Task):
    task_list[index] = task
    # task_list[index] = {
    #     "task": task,
    #     "status": status
    # }
    return {'tasks': task_list}


@router.delete('/')
def delete(index: int):
    del task_list[index]
    return {'tasks': task_list}

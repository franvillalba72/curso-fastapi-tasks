# Router for task
from fastapi import APIRouter, status, Path, Body, Depends
from sqlalchemy.orm import Session

# Importamos el conector a la base de datos y el método para obtener la sesión
from database.database import get_database_session
from database.task import crud
from schemes import Task, TaskRead, TaskWrite
from dataexample import task_with_ORM

router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK)
def get(db: Session = Depends(get_database_session)):
    tasks = crud.getAll(db=db)

    # Devolvemos el casteo de los objetos de la base de datos a objetos de la clase Task (Pydantic)
    return {'tasks': [TaskRead.from_orm(task) for task in tasks]}


@router.get('/{id}', status_code=status.HTTP_200_OK)
def getById(id: int = Path(ge=1), db: Session = Depends(get_database_session)):
    # Devolvemos un objeto de la base de datos
    # return crud.getById(db=db, id=id)

    # En vez de devolver un objeto de la base de datos, devolvemos un objeto de la clase Task (Pydantic)
    return Task.from_orm(crud.getById(db=db, id=id))


@router.post('/', status_code=status.HTTP_201_CREATED)
def add(task: TaskWrite = Body(example=task_with_ORM), db: Session = Depends(get_database_session)):
    taskdb = crud.create(db=db, task=task)

    return {'task': TaskWrite.from_orm(taskdb)}


@router.put('/{id}', status_code=status.HTTP_200_OK)
def update(id: int = Path(ge=1), task: TaskWrite = Body(example=task_with_ORM), db: Session = Depends(get_database_session)):
    result = crud.update(db=db, id=id, task=task)

    return result


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete(id: int = Path(ge=1), db: Session = Depends(get_database_session)):
    task_db = crud.delete(db=db, id=id)

    return {'task': task_db}


@router.post('/tag/{tag_id}/{task_id}', status_code=status.HTTP_200_OK)
def tagAdd(tag_id: int = Path(ge=1), task_id: int = Path(ge=1), db: Session = Depends(get_database_session)):
    result = crud.tagAdd(db, tag_id, task_id)

    return result


@router.delete('/tag/{tag_id}/{task_id}', status_code=status.HTTP_200_OK)
def tagAdd(tag_id: int = Path(ge=1), task_id: int = Path(ge=1), db: Session = Depends(get_database_session)):
    result = crud.tagRemove(db, tag_id, task_id)

    return result

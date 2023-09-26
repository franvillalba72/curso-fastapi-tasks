from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from database import models
from schemes import Task
from database.pagination import paginate, PageParams


def getAll(db: Session):
    tasks = db.query(models.Task).all()
    return tasks


def getById(db: Session, id: int):
    task = db.query(models.Task).get(id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {id} not found"
        )
    return task


def getByCategoryId(db: Session, id: int):
    # Búsqueda por relación invertida
    tasks = db.query(models.Category).get(id).tasks
    return tasks


def create(db: Session, task: Task):
    taskdb = models.Task(
        name=task.name,
        description=task.description,
        status=task.status,
        category_id=task.category_id,
        user_id=task.user_id,
    )
    try:
        db.add(taskdb)
        db.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Task {task.name} already exists",
        )

    db.refresh(taskdb)  # Esto es opcional porque no lo vamos a usar ahora
    return taskdb


def update(db: Session, id: int, task: Task):
    taskdb = getById(db=db, id=id)

    try:
        taskdb.name = task.name
        taskdb.description = task.description
        taskdb.status = task.status
        taskdb.category_id = task.category_id
        taskdb.user_id = task.user_id
        db.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Error in update"
        )

    return {"Success": f"Task {taskdb.id} updated"}


def delete(db: Session, id: int):
    taskdb = getById(db, id)
    db.delete(taskdb)
    db.commit()

    return taskdb


def pagination(page: int, size: int, db: Session):
    page_params = PageParams()
    page_params.page = page
    page_params.size = size
    return paginate(page_params, db.query(models.Task), Task)


# *************** TAGS ********************************
def getTagById(db: Session, id: int):
    tag = db.query(models.Tag).get(id)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Tag {id} not found"
        )

    return tag


def tagAdd(db: Session, id: int, task_id: int):
    taskdb = getById(db, task_id)
    tag = getTagById(db, id)

    taskdb.tags.append(tag)
    db.commit()

    return {"Success": f"Tag {tag.id} added to task {taskdb.id}"}


def tagRemove(db: Session, id: int, task_id: int):
    taskdb = getById(db, task_id)
    tag = getTagById(db, id)

    taskdb.tags.remove(tag)
    db.commit()

    return {"Success": f"Tag {tag.id} removed from task {taskdb.id}"}

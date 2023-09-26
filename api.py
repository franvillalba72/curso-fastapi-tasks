import uvicorn
from fastapi import FastAPI, APIRouter, Query, Path, Depends
from sqlalchemy.orm import Session

from task import router as task_router
from myupload import upload_router

from database.database import Base, engine, get_database_session
from database.models import Task

app = FastAPI()
router = APIRouter()

# Creamos las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)


@router.get('/hello')
# Con el Depends indicamos que no son parámetros que se van a recibir por el query
def hello_world(db: Session = Depends(get_database_session)):
    return {'Hola': 'world'}


@app.get("/e_phone")
def phone(phone: str = Query(pattern=r"^(\(?\+[\d]{1,3}\)?)\s?([\d]{1,5})\s?([\d][\s\.-]?){6,7}$")):
    return {"phone": phone}


@app.get("/ep_phone/{phone}")  # +34 111 12-34-56
def phone(phone: str = Path(pattern=r"^(\(?\+[\d]{1,3}\)?)\s?([\d]{1,5})\s?([\d][\s\.-]?){6,7}$",
                            example="+34 123 12-34-56")):
    return {"phone": phone}


app.include_router(router=router)
app.include_router(router=task_router, prefix='/tasks')
app.include_router(router=upload_router, prefix='/upload')


if __name__=="__main__":
    uvicorn.run("api:app", port=8000, reload=True)

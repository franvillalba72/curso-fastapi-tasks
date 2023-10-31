import uvicorn
from fastapi import FastAPI, APIRouter, Query, Path, Depends, Header, status
from fastapi.security import APIKeyHeader
from typing import Optional, Annotated
from sqlalchemy.orm import Session

from task import router as task_router
from myupload import upload_router
from user import user_router

from database.database import Base, engine, get_database_session
from database.models import Task, User, AccessToken
from fastapi import HTTPException, Request
from authentication.authentication import verify_access_token
import time

app = FastAPI()
router = APIRouter()

# Creamos las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)


# Middlewares
# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     print(process_time)
#     return response


# Tokens Auth no BD
API_KEY_TOKEN = "SECRET_PASSWORD"
api_key_token = APIKeyHeader(name='Token')


@app.get("/protected-route")
def protected_route(token: str = Depends(api_key_token)):
    if token != API_KEY_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"message": "You are authenticated"}


@router.get('/hello')
# Con el Depends indicamos que no son parámetros que se van a recibir por el query
def hello_world(user=Depends(verify_access_token), db: Session = Depends(get_database_session)):
    return {'User': user}


@app.get("/e_phone")
def phone(phone: str = Query(pattern=r"^(\(?\+[\d]{1,3}\)?)\s?([\d]{1,5})\s?([\d][\s\.-]?){6,7}$")):
    return {"phone": phone}


@app.get("/ep_phone/{phone}")  # +34 111 12-34-56
def phone(phone: str = Path(pattern=r"^(\(?\+[\d]{1,3}\)?)\s?([\d]{1,5})\s?([\d][\s\.-]?){6,7}$",
                            example="+34 123 12-34-56")):
    return {"phone": phone}


# Dependencias en el query
def pagination(page: Optional[int] = 1, limit: Optional[int] = 10) -> dict:
    return {"page": page-1, "limit": limit}


@app.get("/p-task")
def index(pagination: dict = Depends(pagination)):
    return pagination


# Dependencias en el path
def validate_token(token: str = Header()):
    if token != "123456":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@app.get("/route-protected", dependencies=[Depends(validate_token)])
def protected_route(index: int):
    return {"index": index}


# Dependencias en anotaciones (variables)
CurrentTaskId = Annotated[int, Depends(validate_token)]


@app.get("/route-protected2")
def protected_route2(token: CurrentTaskId, index: int):
    return {"index": index}


app.include_router(router=router)
app.include_router(router=task_router, prefix='/tasks', tags=['Tasks'])
app.include_router(router=upload_router, prefix='/upload', tags=['Upload'])
app.include_router(router=user_router, tags=['User'])


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)

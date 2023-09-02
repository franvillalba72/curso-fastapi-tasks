from fastapi import FastAPI, APIRouter, Query, Path
from task import router as task_router

app = FastAPI()
router = APIRouter()


@router.get('/hello')
def hello_world():
    return {'Hola': 'world'}


@app.get("/e_phone")
def phone(phone: str = Query(pattern=r"^(\(?\+[\d]{1,3}\)?)\s?([\d]{1,5})\s?([\d][\s\.-]?){6,7}$")):
    return {"phone": phone}


@app.get("/ep_phone/{phone}")  # +34 111 12-34-56
def phone(phone: str = Path(pattern=r"^(\(?\+[\d]{1,3}\)?)\s?([\d]{1,5})\s?([\d][\s\.-]?){6,7}$")):
    return {"phone": phone}


app.include_router(router=router)
app.include_router(router=task_router, prefix='/tasks')

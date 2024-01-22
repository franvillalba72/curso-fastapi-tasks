from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemes import UserCreate
from authentication import password, authentication
from database import database, models

user_router = APIRouter()


@user_router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(database.get_database_session)):
    # Comprobamos que las contraseñas coinciden
    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")

    # Comprobamos que el usuario no existe
    user_exists = db.query(models.User).filter(
        models.User.email == user.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Creamos el usuario
    hashed_password = password.get_password_hash(user.password)

    user_db = models.User(name=user.name, surname=user.surname, email=user.email,
                          website=user.website, hashed_password=hashed_password)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return user_db


@user_router.post("/token")
def create_token(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm), db: Session = Depends(database.get_database_session)):
    email = form_data.username
    password = form_data.password
    user = authentication.authenticate(email, password, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    return authentication.create_access_token(user, db)


@user_router.delete("/logout", status_code=status.HTTP_200_OK, dependencies=[Depends(authentication.logout)])
def logout():
    return {"message": "Logout successful"}

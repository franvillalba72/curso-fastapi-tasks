from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from datetime import datetime, timedelta
from database.database import get_database_session
from database.models import User, AccessToken
from authentication.password import verify_password, generate_token


api_key_token = APIKeyHeader(name='Token')


def authenticate(email: str, password: str, db: Session) -> User | None:
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def create_access_token(user: User, db: Session) -> AccessToken:
    # Verificamos si ya existe un token para ese usuario
    access_token = db.query(AccessToken).join(User).filter(
        AccessToken.user_id == user.id).first()

    # Si existe y ya expiro lo eliminamos y si no expiro lo devolvemos
    if access_token:
        if datetime.now() > access_token.expiration_date:
            db.delete(access_token)
            db.commit()
        else:
            return access_token

    # Si no existe lo creamos
    tomorrow = datetime.now() + timedelta(days=1)

    access_token = AccessToken(
        user_id=user.id, expiration_date=tomorrow,  access_token=generate_token())

    db.add(access_token)
    db.commit()
    db.refresh(access_token)

    return access_token


auth_schema = OAuth2PasswordBearer(tokenUrl='/token')


# def verify_access_token(token: str = Depends(auth_schema), db: Session = Depends(get_database_session)):
def verify_access_token(token: str = Depends(api_key_token), db: Session = Depends(get_database_session)):
    access_token = db.query(AccessToken).join(User).filter(
        AccessToken.access_token == token).first()
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    if datetime.now() > access_token.expiration_date:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Token expired")

    return access_token.user


def logout(token: str = Depends(api_key_token), db: Session = Depends(get_database_session)):
    access_token = db.query(AccessToken).join(User).filter(
        AccessToken.access_token == token).first()
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

    db.delete(access_token)
    db.commit()

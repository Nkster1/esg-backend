from fastapi import APIRouter
from fastapi import Request, Response

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm


from datetime import timedelta
from . import crud, schemas
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests

from starlette.config import Config
from authlib.integrations.starlette_client import OAuth, OAuthError

from .models import User
from .utils import (
    get_db,
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    verify_googletoken
)

GOOGLE_CLIENT_ID = "425079686292-03pl5u5lm36tljmfea8kpkaio7od04vq.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"


routerAuth = APIRouter(prefix="/auth")

@routerAuth.post("/token", response_model=schemas.Token)
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@routerAuth.post("/signup-google", response_model=schemas.Token)
async def create_user_google(request: Request, db: Session = Depends(get_db)):
    token = await request.json()
    token = await verify_googletoken(token['access_token'])
    if token is None:
        raise HTTPException(status_code=400, detail="Corrupted Google Token")
    
    db_user = crud.get_user_by_email(db, email=token['email'])
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(db=db, user=schemas.UserCreate(email=token['email'], password="GOOGLE"))

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@routerAuth.post("/signup", response_model=schemas.Token)
async def create_user_google(request: Request, db: Session = Depends(get_db)):
    token = await request.json()
    db_user = crud.get_user_by_email(db, email=token['email'])
    if db_user:
        user = authenticate_user(db, token['email'], "GOOGLE")
        if user:
            raise HTTPException(status_code=400, detail="Email already registered with an Google Account")
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(db=db, user=schemas.UserCreate(email=token['email'], password=token['password']))

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@routerAuth.post("/login-google", response_model=schemas.Token)
async def create_user_google(request: Request, db: Session = Depends(get_db)):
    token = await request.json()
    token = await verify_googletoken(token['access_token'])
    if token is None:
        raise HTTPException(status_code=400, detail="Corrupted Google Token")
    
    db_user = crud.get_user_by_email(db, email=token['email'])
    if not db_user: raise HTTPException(status_code=400, detail="Unregistered user. Please go to signup page.")

    user = authenticate_user(db, db_user.email, "GOOGLE")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@routerAuth.post("/login", response_model=schemas.Token)
async def create_user_google(request: Request, db: Session = Depends(get_db)):
    token = await request.json()

    db_user = crud.get_user_by_email(db, email=token['email'])
    if not db_user: raise HTTPException(status_code=400, detail="Unregistered user. Please go to signup page.")

    user = authenticate_user(db, db_user.email, password=token['password'])
    if not user: raise HTTPException(status_code=400, detail="Wrong password.")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@routerAuth.post("/signup", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

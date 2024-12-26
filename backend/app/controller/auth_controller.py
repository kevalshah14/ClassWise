# Controller: Handles HTTP requests and responses

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from app.service.auth_service import AuthService
from app.config import db

auth_router = APIRouter()

# Dependency to get the database session
async def get_session():
    async with db.get_session() as session:
        yield session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    service = AuthService(None)
    try:
        payload = service.verify_jwt_token(token)
        return payload
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

@auth_router.post("/auth/google/")
async def login_with_google(google_token: str, session: AsyncSession = Depends(get_session)):
    """
    Login with Google OAuth.
    """
    service = AuthService(session)
    try:
        token = await service.login_with_google(google_token)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.post("/auth/login/")
async def login_with_email(email: str, password: str, session: AsyncSession = Depends(get_session)):
    """
    Login with email and password.
    """
    service = AuthService(session)
    try:
        token = await service.login_with_email(email, password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.post("/auth/signup/")
async def sign_up_with_email(name: str, email: str, password: str, session: AsyncSession = Depends(get_session)):
    """
    Sign up with name, email, and password.
    """
    service = AuthService(session)
    try:
        auth = await service.sign_up_with_email(name, email, password)
        return {"message": "User successfully registered.", "user": auth}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.get("/auth/verify/")
async def verify_token(token: str):
    """
    Verify a JWT token.
    """
    service = AuthService(None)  # No session needed for token verification
    try:
        payload = service.verify_jwt_token(token)
        return {"message": "Token is valid", "user": payload}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

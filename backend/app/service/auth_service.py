# Service: Implements business logic

from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.repository.auth_repository import AuthRepository
from app.model.models import Auth
import httpx
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, AsyncSession


class AuthService:
    def __init__(self, session: AsyncSession):
        self.repo = AuthRepository(session)

    async def login_with_google(self, google_token: str) -> str:
        # Validate Google token and fetch user info
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://oauth2.googleapis.com/tokeninfo",
                params={"id_token": google_token}
            )
            if response.status_code != 200:
                raise ValueError("Invalid Google token.")
            google_data = response.json()

        google_id = google_data.get("sub")
        email = google_data.get("email")

        if not google_id or not email:
            raise ValueError("Invalid Google token data.")

        # Check or create user
        auth = await self.repo.get_by_google_id(google_id)
        if not auth:
            auth = await self.repo.create_with_google(email=email, google_id=google_id)

        return self.create_jwt_token(auth)

    async def login_with_email(self, email: str, password: str) -> str:
        # Validate email and password
        auth = await self.repo.get_by_email(email)
        if not auth or auth.password != password:  # Use hashed passwords in production
            raise ValueError("Invalid credentials.")
        
        return self.create_jwt_token(auth)

    async def sign_up_with_email(self, name: str, email: str, password: str) -> Auth:
        # Check if the email is already registered
        existing_auth = await self.repo.get_by_email(email)
        if existing_auth:
            raise ValueError("Email already registered.")

        # Create a new user
        return await self.repo.create_with_email(name, email, password)

    def create_jwt_token(self, auth: Auth) -> str:
        data = {
            "sub": str(auth.id),
            "email": auth.email,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    def verify_jwt_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise ValueError("Invalid or expired token.")

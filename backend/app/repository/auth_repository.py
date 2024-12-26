
# Repository: Handles database queries

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.model.models import Auth

class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Auth:
        result = await self.session.execute(select(Auth).where(Auth.email == email))
        return result.scalar()

    async def get_by_google_id(self, google_id: str) -> Auth:
        result = await self.session.execute(select(Auth).where(Auth.google_id == google_id))
        return result.scalar()

    async def create_with_google(self, email: str, google_id: str) -> Auth:
        auth = Auth(email=email, google_id=google_id)
        self.session.add(auth)
        await self.session.commit()
        await self.session.refresh(auth)
        return auth

    async def create_with_email(self, name: str, email: str, password: str) -> Auth:
        auth = Auth(name=name, email=email, password=password)
        self.session.add(auth)
        await self.session.commit()
        await self.session.refresh(auth)
        return auth
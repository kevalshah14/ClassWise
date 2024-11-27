# app/model/models.py

from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class Auth(SQLModel, table=True):
    __tablename__ = "auth"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)

    user: Optional["User"] = Relationship(back_populates="auth", sa_relationship_kwargs={"uselist": False})


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    phone_number: Optional[str] = Field(default=None, nullable=True)
    auth_id: int = Field(foreign_key="auth.id", nullable=False)

    auth: Optional[Auth] = Relationship(back_populates="user")
    notifications: List["Notification"] = Relationship(back_populates="user")


class Class(SQLModel, table=True):
    __tablename__ = "class"

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True, nullable=False)
    name: str = Field(nullable=False)
    availability: int = Field(default=0, nullable=False)

    notifications: List["Notification"] = Relationship(back_populates="class_")


class Notification(SQLModel, table=True):
    __tablename__ = "notification"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    class_id: int = Field(foreign_key="class.id", nullable=False)
    is_active: bool = Field(default=True, nullable=False)

    user: Optional[User] = Relationship(back_populates="notifications")
    class_: Optional[Class] = Relationship(back_populates="notifications")

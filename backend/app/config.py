# app/config.py

import os
import asyncpg  # Import asyncpg
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlalchemy import text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables for default database
DEFAULT_DB_USER = os.getenv('DEFAULT_DB_USER', 'postgres')
DEFAULT_DB_PASSWORD = os.getenv('DEFAULT_DB_PASSWORD', 'postgres')
DEFAULT_DB_HOST = os.getenv('DEFAULT_DB_HOST', 'localhost')
DEFAULT_DB_PORT = os.getenv('DEFAULT_DB_PORT', '5432')
DEFAULT_DB_NAME = os.getenv('DEFAULT_DB_NAME', 'postgres')  # Default database

# Retrieve environment variables for target database
TARGET_DB_USER = os.getenv('TARGET_DB_USER', 'postgres')
TARGET_DB_PASSWORD = os.getenv('TARGET_DB_PASSWORD', 'postgres')
TARGET_DB_HOST = os.getenv('TARGET_DB_HOST', 'localhost')
TARGET_DB_PORT = os.getenv('TARGET_DB_PORT', '5432')
TARGET_DB_NAME = os.getenv('TARGET_DB_NAME', 'dequeue_db')  # Your application database

# Construct database URLs
DEFAULT_DB_CONFIG = f'postgresql+asyncpg://{DEFAULT_DB_USER}:{DEFAULT_DB_PASSWORD}@{DEFAULT_DB_HOST}:{DEFAULT_DB_PORT}/{DEFAULT_DB_NAME}'
TARGET_DB_CONFIG = f'postgresql+asyncpg://{TARGET_DB_USER}:{TARGET_DB_PASSWORD}@{TARGET_DB_HOST}:{TARGET_DB_PORT}/{TARGET_DB_NAME}'


class AsyncDatabaseSession:

    def __init__(self):
        self.engine = None
        self.async_session_maker = None

    async def init(self):
        """
        Initialize the database by ensuring the target database exists.
        If it doesn't, create it.
        Then, connect to the target database for further operations.
        """
        try:
            # Step 1: Check if the target database exists
            default_engine = create_async_engine(DEFAULT_DB_CONFIG, echo=True)
            async with default_engine.connect() as conn:
                result = await conn.execute(
                    text("SELECT 1 FROM pg_database WHERE datname=:db_name"),
                    {"db_name": TARGET_DB_NAME}
                )
                exists = result.scalar()
            await default_engine.dispose()

            if not exists:
                # Use asyncpg directly to create the database
                conn_params = {
                    "user": DEFAULT_DB_USER,
                    "password": DEFAULT_DB_PASSWORD,
                    "host": DEFAULT_DB_HOST,
                    "port": DEFAULT_DB_PORT,
                    "database": DEFAULT_DB_NAME,
                }
                # Establish the connection
                pg_conn = await asyncpg.connect(**conn_params)
                try:
                    # Terminate existing connections to the target database if any
                    await pg_conn.execute(
                        "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = $1",
                        TARGET_DB_NAME
                    )
                    # Create the target database
                    await pg_conn.execute(f'CREATE DATABASE "{TARGET_DB_NAME}"')
                    print(f"Database '{TARGET_DB_NAME}' created.")
                finally:
                    # Close the connection
                    await pg_conn.close()
            else:
                print(f"Database '{TARGET_DB_NAME}' already exists.")

            # Step 2: Connect to the target database
            self.engine = create_async_engine(TARGET_DB_CONFIG, echo=True)
            self.async_session_maker = sessionmaker(
                self.engine, class_=AsyncSession, expire_on_commit=False
            )
        except Exception as e:
            print(f"Error during database initialization: {e}")
            raise e

    async def create_all(self):
        """
        Create all tables based on the SQLModel models.
        This operation is idempotent.
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def close(self):
        """
        Close the engine connection gracefully.
        """
        await self.engine.dispose()

    def get_session(self) -> AsyncSession:
        """
        Provide a new asynchronous session.
        """
        return self.async_session_maker()


db = AsyncDatabaseSession()


async def commit_or_rollback(session: AsyncSession):
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e

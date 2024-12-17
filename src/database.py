from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = (
    "postgresql+asyncpg://uf49quo3fskjua:p65789759024a9cbfa6b4b94f151ff3f835e7c5f11a00d6433ce9f1db12c53d5b"
    "@c724r43q8jp5nk.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d41fnk62r8b5ok"
)

# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True, pool_size=10, max_overflow=10)

# Session factory for async
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)

# Base class for models
Base = declarative_base()

# Dependency to get the database session
async def get_db():
    async with async_session() as session:
        try:
            # Yield the session for use in DB operations
            yield session
            # Commit any pending changes
            await session.commit()
        except SQLAlchemyError as e:
            # Rollback the session in case of an exception
            await session.rollback()
            raise e  # Re-raise the exception for handling elsewhere
        finally:
            # Close the session (ensures the connection is returned to the pool)
            await session.close()

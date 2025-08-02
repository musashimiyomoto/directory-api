from typing import AsyncGenerator

from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from db.sessions import async_session
from settings import settings

api_key_header = APIKeyHeader(name=settings.API_KEY_NAME, auto_error=False)


async def validate_api_key(api_key: str = Security(api_key_header)) -> str:
    """Validate API key from request header

    Args:
        api_key: API key from request header

    Returns:
        API key if valid

    Raises:
        HTTPException: If API key is invalid or missing

    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="API key is missing"
        )

    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key"
        )

    return api_key


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session

    Yields:
        SQLAlchemy async session

    """
    async with async_session() as session:
        yield session

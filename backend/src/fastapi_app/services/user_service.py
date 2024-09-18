from collections.abc import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.item import Item
from ..models.user import User
from ..schemas.item import ItemCreate
from ..schemas.user import UserCreate


async def get_user_by_email(db_session: AsyncSession, email: str) -> User:
    stmt = select(User).filter(User.email == email)
    result = await db_session.execute(stmt)
    user = result.scalars().first()
    if user:
        raise HTTPException(status_code=403, detail="User Already exists")
    return user


async def get_users(
    db_session: AsyncSession, skip: int = 0, limit: int = 100
) -> Sequence[User]:
    stmt = select(User).offset(skip).limit(limit)
    result = await db_session.execute(stmt)
    users = result.scalars().all()
    return users


async def create_user(db_session: AsyncSession, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db_session.add(db_user)
    await db_session.commit()
    await db_session.refresh(db_user)
    return db_user


async def create_user_item(
    db_session: AsyncSession, item: ItemCreate, user_id: int
) -> Item:
    db_item = Item(title=item.title, description=item.description, owner_id=user_id)
    db_session.add(db_item)
    await db_session.commit()
    await db_session.refresh(db_item)
    return db_item


async def get_user(db_session: AsyncSession, user_id: int) -> User:
    stmt = select(User).where(User.id == user_id)
    result = await db_session.execute(stmt)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

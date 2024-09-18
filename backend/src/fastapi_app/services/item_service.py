from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.item import Item
from ..schemas.item import ItemCreate


async def get_items(db_session: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(Item).offset(skip).limit(limit)
    result = await db_session.execute(stmt)
    items = result.scalars().all()
    return items


async def create_user_item(db_session: AsyncSession, item: ItemCreate, user_id: int):
    db_item = Item(**item.model_dump(), owner_id=user_id)
    db_session.add(db_item)
    await db_session.commit()
    await db_session.refresh(db_item)
    return db_item

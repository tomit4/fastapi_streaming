from collections.abc import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db_session
from ..middlewares.logger import TimedRoute
from ..schemas.item import Item
from ..services.item_service import get_items

router = APIRouter(prefix="/items", tags=["items"], route_class=TimedRoute)


@router.get("/", response_model=list[Item])
async def read_items(
    skip: int = 0, limit: int = 100, db_session: AsyncSession = Depends(get_db_session)
) -> Sequence[Item]:
    items = await get_items(db_session=db_session, skip=skip, limit=limit)
    return items

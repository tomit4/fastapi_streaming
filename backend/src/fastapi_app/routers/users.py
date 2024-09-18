import asyncio
import base64
import json
import os
from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db_session
from ..middlewares.logger import TimedRoute
from ..schemas.item import Item, ItemCreate
from ..schemas.user import User, UserCreate
from ..services.user_service import (
    create_user,
    create_user_item,
    get_user,
    get_user_by_email,
    get_users,
)

router = APIRouter(prefix="/users", tags=["users"], route_class=TimedRoute)


@router.post("/", response_model=User)
async def create_new_user(
    user: UserCreate, db_session: AsyncSession = Depends(get_db_session)
) -> User:
    db_user = await get_user_by_email(db_session, email=user.email)
    if db_user:
        raise HTTPException(status_code=403, detail="Email already registered")
    return await create_user(db_session=db_session, user=user)


@router.get("/", response_model=list[User])
async def read_users(
    skip: int = 0, limit: int = 100, db_session: AsyncSession = Depends(get_db_session)
) -> Sequence[User]:
    users = await get_users(db_session, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: int, db_session: AsyncSession = Depends(get_db_session)
) -> User:
    db_user = await get_user(db_session, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/items/", response_model=Item)
async def create_item_for_user(
    user_id: int, item: ItemCreate, db_session: AsyncSession = Depends(get_db_session)
) -> Item:
    return await create_user_item(db_session=db_session, item=item, user_id=user_id)


IMAGES_DIR = "./images/"


@router.get("/image-count/")
async def get_image_count():
    image_count = len([f for f in os.listdir(IMAGES_DIR) if f.endswith(".webp")])
    return JSONResponse(status_code=200, content={"image_count": image_count})


async def image_streamer():
    for image_filename in os.listdir(IMAGES_DIR):
        if image_filename.endswith(".webp"):
            image_path = os.path.join(IMAGES_DIR, image_filename)
            with open(image_path, "rb") as image_file:
                image_bytes = image_file.read()
                encoded_image = base64.b64encode(image_bytes).decode("utf-8")
                yield encoded_image

        # NOTE: must be at least 0.1, 0 will not flush in time and will not stream
        # await asyncio.sleep(0.1)
        await asyncio.sleep(4)


@router.get("/streaming/")
async def test_streaming() -> StreamingResponse:
    return StreamingResponse(image_streamer(), media_type="application/octet-stream")

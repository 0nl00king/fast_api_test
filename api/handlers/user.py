from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_async_session

from db.data_access_layer.user import UserDAL

from api.schemas.user import (
    UserCreate,
    ShowUser,
)

user_router = APIRouter()


async def _create_new_user(body: UserCreate, session: AsyncSession) -> ShowUser:
    async with session as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email,
            )
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active,
            )


@user_router.post("/", response_model=ShowUser)
async def create_user(
        body: UserCreate,
        session: AsyncSession = Depends(get_async_session)
):
    return await _create_new_user(body, session)
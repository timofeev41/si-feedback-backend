from fastapi import APIRouter, HTTPException

from src.core.dependencies.auth import CurrentUser
from src.core.models.session import StartedSession
from src.core.models.user import User
from src.core.schemas.user import UserUpdateSchema, UserSchema

router = APIRouter(
    prefix="/users",
    tags=["Users Management"],
    dependencies=[StartedSession()],
)


@router.patch("/", response_model=UserSchema)
async def update_user_info(data: UserUpdateSchema, current_user: CurrentUser):
    current_user.full_name = data.full_name
    current_user.position = data.position
    current_user.company = data.company
    current_user.save()

    return current_user


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, _: CurrentUser):
    if user := User.one(User.id == user_id):
        return user
    raise HTTPException(status_code=404, detail="User not found")

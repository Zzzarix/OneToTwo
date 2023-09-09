from typing import Annotated

from fastapi import APIRouter, Depends
from onetotwo.api.validation.user import CreateUser, DeleteUser, UpdateUser
from onetotwo.user.manager import UserManager
from onetotwo.user.model import User

router = APIRouter(prefix="/users", tags=["users"])


def get_user_manager() -> UserManager:
    """Return manager depend"""
    ...


@router.get("/get/{uid}", response_model=User, response_description="Get user by it's uid")
def get_user(uid: str, manager: Annotated[UserManager, Depends(get_user_manager)]):
    """Get user"""
    ...


@router.post("/create", response_model=User, response_description="Create user")
def create_user(schema: CreateUser, manager: Annotated[UserManager, Depends(get_user_manager)]):
    """Create user"""
    ...


@router.post("/update", response_description="Update user")
def update_user(schema: UpdateUser, manager: Annotated[UserManager, Depends(get_user_manager)]):
    """Update user"""
    ...


@router.post("/delete", response_description="Delete user")
def delete_user(schema: DeleteUser, manager: Annotated[UserManager, Depends(get_user_manager)]):
    """Delete user"""
    ...

from pydantic import BaseModel

from onetotwo.user.model import UserLocale

class CreateUser(BaseModel):
    """CreateUser validate model"""

    name: str
    email: str
    password: str
    locale: UserLocale

class UpdateUser(BaseModel):
    """UpdateUser validate model"""

class DeleteUser(BaseModel):
    """DeleteUser validate model"""

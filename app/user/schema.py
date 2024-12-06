from pydantic import BaseModel, Field, field_validator,SecretStr
from typing import Optional
from app.core.type import PydanticObjectId
from app.campus.model import Campus
from bson import ObjectId
from datetime import datetime

class UserSchema(BaseModel):
    id: PydanticObjectId
    username: str
    password: SecretStr
    display_name: str
    mobile: Optional[str] = None
    campus: PydanticObjectId
    created_at: datetime

    @field_validator("id", mode="before")
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v   

    @field_validator("campus", mode="before")
    def validate_campus(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, Campus):
            return str(v.id)
        return v

    class Config:
        from_attributes = True
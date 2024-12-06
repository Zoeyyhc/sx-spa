from pydantic import BaseModel,RootModel,field_validator
from app.core.type import PydanticObjectId
from bson import ObjectId


class CampusSchema(BaseModel):
    name: str
    id: PydanticObjectId

    @field_validator("id", mode="before")
    def validate_object_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v  
    
    class Config:
        orm_mode = True
        from_attributes = True
        json_encoders = {
            PydanticObjectId: str, 
        }

class CampusListSchema(RootModel[list[CampusSchema]]):
    class Config:
        orm_mode = True
        from_attributes = True


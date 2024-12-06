
from mongoengine.base.datastructures import BaseList,LazyReference
from typing import Any
from bson import ObjectId
from flask_mongoengine import Document
from pydantic_core import core_schema
from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue

class PydanticObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, source: type, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls.validate, core_schema.str_schema()
        )

    @classmethod
    def validate(cls, value: Any, info: core_schema.ValidationInfo) -> "PydanticObjectId":
        print(f"Validating value: {value} (type: {type(value)})")
        if isinstance(value, dict) and "$oid" in value:
            value = value["$oid"]
        if isinstance(value, ObjectId):
            print(f"Converting ObjectId to string: {value}")
            return cls(str(value))
        if isinstance(value, str) and ObjectId.is_valid(value):
            print(f"Converting valid ObjectId string: {value}")
            return cls(value)
        if not ObjectId.is_valid(value):
            raise ValueError(f"Invalid ObjectId: {value}")
        return cls(str(ObjectId(value)))

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetCoreSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema.update(type="string", format="objectid")
        return json_schema
    
class MongoModel(BaseModel):
    @classmethod
    def _get_value(cls, v: Any,to_dict: bool,**kwargs:Any):
        if to_dict and type(v) is BaseList:
            return list(v)
        return super()._get_value(v,to_dict=to_dict,**kwargs)

class MongoListModel(MongoModel):
    def dict(self, *args, **kwargs):
        return super().dict(*args, **kwargs)["__root__"]
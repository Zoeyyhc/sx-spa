from app.core.types import MongoModel, AllOptional, PydanticObjectId, MongoListModel
from uuid import UUID
from datetime import datetime
from typing import List
import uuid

class LectureSchema(MongoModel):
    id: UUID
    title: str
    stream_url: str
    recording_url: str
    scheduled_time: datetime

class LectureCreateSchema(LectureSchema):
    id: UUID = uuid.uuid4()

class LecturePutSchema(LectureSchema, metaclass = AllOptional):
    pass

class LectureListSchema(MongoListModel):
    __root__: list[LectureSchema]

class CourseSchema(MongoModel):
    id: PydanticObjectId
    name: str
    uni_course_code: str
    description: str
    teacher: PydanticObjectId
    campus: PydanticObjectId
    created_time: datetime
    publish_time: datetime
    original_price: float
    cover_image: str
    lectures: List[LectureSchema]
    enrolled_students: List[PydanticObjectId]

class CourseCreateSchema(MongoModel):
    name: str
    uni_course_code: str
    description: str
    teacher: PydanticObjectId
    campus: PydanticObjectId
    publish_time: datetime = None
    original_price: float = 0.0
    cover_image: str = ""
    lectures: List[LectureSchema] = []
    enrolled_students: List[PydanticObjectId] = []

class CoursePutSchema(MongoModel, metaclass=AllOptional):
    name: str
    description: str
    teacher: PydanticObjectId
    publish_time: datetime = None
    original_price: float = 0.0
    cover_image: str = ""
    
class CourseBasicInfoSchema(MongoModel):
    id: PydanticObjectId
    name: str
    uni_course_code: str
    description: str
    teacher: PydanticObjectId
    campus: PydanticObjectId
    created_time: datetime
    publish_time: datetime
    original_price: float
    cover_image: str

class CourseListSchema(MongoListModel):
    __root__: List[CourseBasicInfoSchema]
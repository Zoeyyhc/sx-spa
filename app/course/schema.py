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
    id: UUID = None

class LecturePutSchema(LectureSchema, metaclass = AllOptional):
    pass

class LectureListSchema(MongoListModel):
    __root__: list[LectureSchema]

class CourseTeacherInfoSchema(MongoModel):
    id: PydanticObjectId
    display_name: str
class CourseCampusInfoSchema(MongoModel):
    id: PydanticObjectId
    name: str
class CourseEnrolledStudentsSchema(MongoModel):
    id: PydanticObjectId
    username: str
    display_name: str
class CourseDetailSchema(MongoModel):
    id: PydanticObjectId
    name: str
    uni_course_code: str
    description: str
    teacher: CourseTeacherInfoSchema    
    campus: CourseCampusInfoSchema
    created_time: datetime
    publish_time: datetime
    original_price: float
    cover_image: str
    lectures: List[LectureSchema]
    enrolled_students: List[CourseEnrolledStudentsSchema]

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
    teacher: CourseTeacherInfoSchema
    campus: CourseCampusInfoSchema
    created_time: datetime
    publish_time: datetime
    original_price: float
    cover_image: str

class CourseListSchema(MongoListModel):
    __root__: List[CourseBasicInfoSchema]
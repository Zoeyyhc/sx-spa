from app.core.service import BaseService
from app.user.model import User, Teacher
from app.course.schema import CourseCreateSchema, CoursePutSchema, LectureSchema, LectureCreateSchema, LecturePutSchema
from app.campus.model import Campus
from app.course.model import Course, Lecture, LectureAttachment
from app.core.storage import upload_file_to_s3
from flask_jwt_extended import get_current_user
import uuid
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import NotFound

class CourseService(BaseService):

    def __init__(self, user:User):
        super().__init__(CourseService.__name__, user)

    def get_courses_query(self, **kwargs):
        if self.user._cls == "User.Admin" and "course_admin" in self.user.permissions:
            return Course.objects(**kwargs)
        if self.user._cls == "User.Teacher":
            return Course.objects(teacher=self.user, **kwargs)
        else:
            return Course.objects(enrolled_students=self.user, **kwargs)

    def create_course(self, course:CourseCreateSchema) -> Course:
        self.logger.info("Creating courses")
        Campus.objects(id=course.campus).first_or_404("Campus not exists")
        Teacher.objects(id=course.teacher).first_or_404("Teacher not exists")
        course = Course(**course.dict())
        return course.save()
    
    def list_courses(self, campus: str = None, teacher: str = None) -> list[Course]:
        self.logger.info("Fetching courses")
        querys: dict  = {}
        if campus is not None:
            querys["campus"] = campus 
        if teacher is not None:
            querys["teacher"] = teacher
        return list(Course.objects(**querys))
    
    def get_course(self, course_id: str) -> Course:
        self.logger.info("Fetching course")
        return self.get_courses_query(id=course_id).first_or_404("Course not exists")
    
    def delete_course(self, course_id: str) -> Course:
        self.logger.info("Deleting course")
        return Course.objects(id=course_id).delete()
    
    def update_course(self, course_id: str, course: CoursePutSchema):
        self.logger.info("Updating course")
        update_dict = course.dict(exclude_none=True, exclude_defaults=True)
        if len(update_dict) == 0:
            return
        Course.objects(id=course_id).first_or_404("Course not exists").update(
            **update_dict
        ) 


    def add_lecture(self, course_id: str, lecture: LectureCreateSchema):
        self.logger.info("Adding lecture")
        lecture.id = uuid.uuid4()
        course: Course = Course.objects(id=course_id).first_or_404("Course not exists")
        course.update(push__lectures=lecture.dict(exclude_none=True))
        return str(lecture.id)

    def list_lectures(self, course_id: str) -> list[Lecture]:
        self.logger.info("Fetching lectures")
        return Course.objects(id=course_id).first_or_404("Course not exists").lectures
    

    def delete_lecture(self, course_id: str, lecture_id: str) -> int:
        self.logger.info("Deleting lecture")
        return (
            Course.objects(id=course_id)
            .filter(lectures__id=lecture_id)
            .update_one(pull__lectures__id=lecture_id)
        )
    
    def update_lecture(self, course_id: str, lecture_id: str, lecture: LecturePutSchema):
        self.logger.info("Updating lecture")
        update_action = {
            f"set__lectures__S__{key}": value
            for key, value in lecture.dict(exclude_defaults=True).items()
        } # __S__ represents updating the matched record in the filter
        return (
            Course.objects(id=course_id)
            .filter(lectures__id=lecture_id)
            .update_one(**update_action)
        )

    def upload_lecture_attachment(
        self, course_id: str, lecture_id: str, file: FileStorage, file_type: str, name
    ):
        course: Course = Course.objects(id=course_id).first_or_404("Course not exists")
        lecture: Lecture = course.lectures.filter(id=lecture_id).first()
        if lecture is None:
            raise NotFound("Lecture not exists")

        url = upload_file_to_s3(
            file, f"courses/{course_id}/lectures/{lecture_id}/attachments"
        )
        attachment = LectureAttachment(
            name=name is not None and name or file.filename,
            filename=file.filename,
            type=file_type,
            bucket_url=url,
        )
        Course.objects(id=course_id).filter(lectures__id=lecture_id).update_one(
            push__lectures__S__attachments=attachment
        )

    def delete_attachment(self, course_id: str, lecture_id: str, filename: str):
        course: Course = Course.objects(id=course_id).first_or_404("Course not exists")
        lecture: Lecture = course.lectures.filter(id=lecture_id).first()

        if lecture is None:
            raise NotFound("Lecture not exists")

        del_num = lecture.attachments.filter(filename=filename).delete()
        course.save()
        return del_num, 200
    
def course_service() -> CourseService:
    print("current user is: ", get_current_user())
    return CourseService(get_current_user())
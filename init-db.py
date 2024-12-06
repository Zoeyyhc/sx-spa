from app import create_app
from app.campus.model import Campus
from app.user.model import User, Student, Admin, Teacher, get_hashed_password
from mongoengine import get_db

print("Loading...")

from app import create_app
from app.campus.model import Campus

create_app()

print("Configuiring database...")
Campus.objects.delete()
User.objects.delete()
print("Finished deleting")

clayton_campus: Campus = Campus(name="Clayton")
clayton_campus.save()

admin = Admin(
    username="admin",
    password=get_hashed_password("admin"),
    display_name="Admin1",
    permissions=["sys-owner","campus_admin","course_admin"],
    mobile="123456789",
    campus = clayton_campus,
)
admin.save()

student = Student(
    username="student_1234555",
    password=get_hashed_password("student"),
    display_name="Jone smith",
    campus=clayton_campus,
    wx="student's wx",
    mobile="123456789",
)

student.save()

teacher = Teacher(
    username="teacher_1234",
    password=get_hashed_password("teacher"),
    display_name="Zoey",
    campus=clayton_campus,
    adn="t4371999"
)

teacher.save()

print("Finished initializing database")
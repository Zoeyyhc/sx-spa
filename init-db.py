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
    permissions=["sys_owner","campus_admin","course_admin","users_admin"],
    mobile="123456789",
    campus = clayton_campus,
)
admin.save()

support = Admin(
    username="support",
    display_name="Support A",
    password=get_hashed_password("support"),
    mobile="123",
    permissions=["course_admin"],
    campus=clayton_campus,
)
support.save()

student = Student(
    username="student",
    password=get_hashed_password("student"),
    display_name="Jone smith",
    campus=clayton_campus,
    wx="student's wx",
    mobile="123456789",
    uni = "Monash University"   
)

student.save()

teacher = Teacher(
    username="teacher",
    password=get_hashed_password("teacher"),
    display_name="Teacher A",
    campus=clayton_campus
)

teacher.save()

print("Finished initializing database")
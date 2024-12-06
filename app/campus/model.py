from flask_mongoengine import Document 
from mongoengine import StringField


class Campus(Document): 
    name: StringField = StringField(required=True)
    

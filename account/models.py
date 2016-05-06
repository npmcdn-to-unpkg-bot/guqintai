from __future__ import unicode_literals
from datetime import datetime


# Create your models here.
import mongoengine
from mongoengine import IntField, DateTimeField, StringField

# Create your models here.
class Account(mongoengine.Document):
 
    username = StringField(required=True)
    email = StringField()
    mobile_number = StringField()
    status = IntField()
    create_time = mongoengine.DateTimeField(default=datetime.now)
    password = StringField()


    meta = {
        'collection': 'account',
    }
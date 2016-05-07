from datetime import datetime


# Create your models here.
import mongoengine
from mongoengine import IntField, DateTimeField, StringField, ListField

# Create your models here.
class Article(mongoengine.Document):
 
    account_id = StringField(required=True)
    username = StringField()
    title = StringField()
    head_image = StringField()
    content = StringField()
    status = IntField()
    category =  IntField()
    tag =  ListField(StringField())
    create_time = mongoengine.DateTimeField(default=datetime.now)

    meta = {
        'collection': 'article',
    }

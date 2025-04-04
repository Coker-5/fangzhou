from mongoengine import Document, ObjectIdField, ListField, StringField, DictField, IntField


# Create your models here.

class cars_data(Document):
    _id=ObjectIdField()
    bottom_left=ListField()
    bottom_right=StringField()
    center_data=DictField()
    center_left1=ListField()
    center_left2=StringField()
    center_right1=ListField()
    center_right2=ListField()
    doc_exist=IntField()
    head_info=DictField()

    meta={
        'collection': 'fangzhou',
        'strict': False
    }
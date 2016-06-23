from peewee import CharField, DateTimeField
from flask_login import UserMixin
from hashlib import sha1
from time import mktime
import datetime
from models.base import BaseModel


class User(BaseModel, UserMixin):

    created = DateTimeField(default=datetime.datetime.now)
    email = CharField(max_length=50)
    password = CharField(max_length=50)

    @staticmethod
    def create(email, password, fullname=None):
        user = User(email=email)
        user.password = sha1(password.encode('utf-8')).hexdigest()
        return user

    def check(self, password):
        return self.password == sha1(password.encode('utf-8')).hexdigest()

    def to_json(self):
        return {
            'id': self.id,
            'created': mktime(self.created.timetuple()) * 1000,
            'email': self.email
        }

from peewee import CharField, ForeignKeyField
from models.user import User
from models.base import BaseModel


class Category(BaseModel):

    text = CharField(max_length=100)
    user = ForeignKeyField(User, related_name='category')

    def to_json(self):
        return {
            'id': self.id,
            'text': self.text
        }

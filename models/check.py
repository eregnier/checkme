from peewee import CharField, ForeignKeyField, DateTimeField, \
    IntegerField, BooleanField
import datetime
from models.category import Category
from models.base import BaseModel


class Check(BaseModel):

    created = DateTimeField(default=datetime.datetime.now)
    check = BooleanField(default=False)
    cross = BooleanField(default=False)
    text = CharField(max_length=100)
    # P = pending, A = archived
    status = CharField(max_length=1, default='P')
    category = ForeignKeyField(Category, related_name='category')
    priority = IntegerField(default=1)

    def to_json(self):
        return {
            'id': self.id,
            'check': self.check,
            'cross': self.cross,
            'text': self.text,
            'category': self.category.to_json(),
            'created': self.created,
            'priority': self.priority
        }

    @staticmethod
    def archive(categoryId):
        checks_to_archive = Check.select().where(
            (Check.check == True) & (Check.category == categoryId)
        )
        for check in checks_to_archive:
            check.status = 'A'
            check.save()

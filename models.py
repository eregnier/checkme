#! /usr/bin/python
# encoding: utf-8
from peewee import SqliteDatabase, Model, CharField, DateTimeField, \
   BooleanField, ForeignKeyField
import datetime

dbname = 'checkme.sqlite'
db = SqliteDatabase(dbname, threadlocals=True)


class Category(Model):

    class Meta:
        database = db

    text = CharField(max_length=100)

    def to_json(self):
        return {
            'id': self.id,
            'text': self.text
        }


class Check(Model):

    class Meta:
        database = db

    created = DateTimeField(default=datetime.datetime.now)
    check = BooleanField(default=False)
    cross = BooleanField(default=False)
    text = CharField(max_length=100)
    # P = pending, A = archived
    status = CharField(max_length=1, default='P')
    category = ForeignKeyField(Category, related_name='category')

    def to_json(self):
        return {
            'id': self.id,
            'check': self.check,
            'cross': self.cross,
            'text': self.text,
            'category': self.category.to_json(),
            'created': self.created
        }

    @staticmethod
    def archive(categoryId):
        checks_to_archive = Check.select().where(
            (Check.check == True) & (Check.category == categoryId)
        )
        with db.atomic():
            for check in checks_to_archive:
                check.status = 'A'
                check.save()




if __name__ == '__main__':

    db.connect()
    db.create_tables([Check, Category], safe=True)

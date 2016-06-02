#! /usr/bin/python
# encoding: utf-8
from peewee import SqliteDatabase, Model, CharField, DateTimeField, \
   BooleanField
import datetime

dbname = 'checkme.sqlite'
db = SqliteDatabase(dbname, threadlocals=True)


class Check(Model):

    class Meta:
        database = db

    created = DateTimeField(default=datetime.datetime.now)
    check = BooleanField(default=False)
    cross = BooleanField(default=False)
    text = CharField(max_length=100)
    # P = pending, A = archived
    status = CharField(max_length=1, default='P')

    def to_json(self):
        return {
            'id': self.id,
            'check': self.check,
            'cross': self.cross,
            'text': self.text
        }

    @staticmethod
    def archive():
        checks_to_archive = Check.select().where(
            Check.check == True
        )
        with db.atomic():
            for check in checks_to_archive:
                check.status = 'A'
                check.save()


if __name__ == '__main__':

    db.connect()
    db.create_tables([Check], safe=True)

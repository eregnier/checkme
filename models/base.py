from peewee import Model, SqliteDatabase


def get_database():
    dbname = 'checkme.sqlite'
    return SqliteDatabase(dbname, threadlocals=True)


class BaseModel(Model):
    class Meta:
        database = get_database()

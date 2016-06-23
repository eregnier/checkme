#! /usr/bin/python
# encoding: utf-8
from models.category import Category
from models.user import User
from models.check import Check
from models.base import get_database
import sys


if __name__ == '__main__':
    if 'create' in sys.argv:
        print 'Creating database... .'
        db = get_database()
        db.connect()
        db.create_tables([User, Check, Category], safe=True)
        print 'Creating database complete.'
    elif 'fixtures' in sys.argv:
        User.create('fake@email.com', 'pass').save()
        User.create('fake1@email.com', 'pass1').save()
    elif 'count' in sys.argv:
        print 'User', User.select().count()
        print 'Category', Category.select().count()
        print 'Check', Check.select().count()
    else:
        print 'Available actions are [create, fixtures, count]'

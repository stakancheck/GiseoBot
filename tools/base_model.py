from peewee import *
from decouple import config


path = config('PATH_P')

# connect base
database = SqliteDatabase(f'{path}\\data\\basic\\data.db')


class User(Model):
    chat_id = IntegerField(primary_key=True)
    login = TextField()
    password = TextField()
    place = TextField()
    town = TextField()
    type_school = TextField()
    school = TextField()
    theme = TextField()
    date_update = DateTimeField()

    class Meta:
        database = database


class FinalMarks(Model):
    chat_id = ForeignKeyField(User)
    subject = TextField()
    quarter_1 = IntegerField()
    quarter_2 = IntegerField()
    quarter_3 = IntegerField()
    quarter_4 = IntegerField()
    final_mark = IntegerField()

    class Meta:
        database = database


class MiddleMarksYear(Model):
    chat_id = ForeignKeyField(User)
    subject = TextField()
    marks = TextField()

    class Meta:
        database = database


class MiddleMarksPeriod(Model):
    chat_id = ForeignKeyField(User)
    subject = TextField()
    period = IntegerField()
    marks = TextField()

    class Meta:
        database = database


class Schedule(Model):
    chat_id = ForeignKeyField(User)
    time = TextField()
    subject = TextField()
    day = IntegerField()
    homework = TextField()

    class Meta:
        database = database


class Duty(Model):
    chat_id = ForeignKeyField(User)
    subject = TextField()
    task = TextField()
    date = TextField()

    class Meta:
        database = database


if __name__ == '__main__':
    FinalMarks.create_table()
    MiddleMarksPeriod.create_table()
    MiddleMarksYear.create_table()
    Schedule.create_table()
    Duty.create_table()
    print('Completed')

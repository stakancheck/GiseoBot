#  Copyright 2023. Artem Sukhanov
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  SPDX-License-Identifier: GPL-3.0-or-later

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

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


database = SqliteDatabase('base.db')


class User(Model):
    user_id = IntegerField(primary_key=True)
    name_user = TextField()
    theme = TextField()

    class Meta:
        database = database


class Marks(Model):
    user_id = ForeignKeyField(User, primary_key=True, related_name='marks')
    subject = TextField()
    quarter_1 = IntegerField()
    quarter_2 = IntegerField()
    quarter_3 = IntegerField()
    quarter_4 = IntegerField()
    final_mark = IntegerField()

    class Meta:
        database = database


class GiseoInfo(Model):
    user_id = ForeignKeyField(User, primary_key=True, related_name='info')
    school = TextField()
    login = TextField()
    password = TextField()

    class Meta:
        database = database


if __name__ == '__main__':
    pass
    User.create_table()
    Marks.create_table()
    GiseoInfo.create_table()
    print(User.select().where(User.user_id == 11111110).get)
    # user_1 = User.create(user_id=11111110, name_user='alex', theme='dark')
    # user_2 = User.create(user_id=22222220, name_user='herb', theme='light')
    # user_3 = User.create(user_id=33333330, name_user='laura', theme='dark')
    # inf_1 = GiseoInfo.create(user_id=user_1, school='test1', login='login1', password='pass1')
    # inf_3 = GiseoInfo.create(user_id=user_3, school='test3', login='login3', password='pass3')
    # marks1 = Marks.create(user_id=user_1, subject='ttt', quarter_1=1, quarter_2=1, quarter_3=1, quarter_4=1, final_mark=1)
    # marks2 = Marks.create(user_id=user_2, subject='ttt', quarter_1=2, quarter_2=2, quarter_3=2, quarter_4=2, final_mark=2)

    # user_1 = User.select().where(User.user_id == 11111110).get()
    # info_1 = GiseoInfo.select().join(User).where(User.user_id == 11111110).get()
    # info_1.login = 'login_test'
    # info_1.save()
    # print(user_1.name_user, info_1.login)



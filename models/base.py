# -*- coding: utf-8 -*-
import peewee


database = peewee.SqliteDatabase('models/xueqiu.db')


class Model(peewee.Model):

    class Meta:
        database = database


class People(Model):

    id = peewee.IntegerField()
    uid = peewee.CharField()
    user_name = peewee.CharField()

    @classmethod
    def remove_duplicate(cls):
        sql = 'delete from people where uid in ( select uid from people '\
            'group by uid having count(id) > 1) and id not in '\
            '(select min(id) from people group by uid having count(id) > 1);'
        database.execute_sql(sql)

    @classmethod
    def remove_all(cls):
        sql = 'delete from people'
        database.execute_sql(sql)


class Chat(Model):
    id = peewee.IntegerField()
    chatting_id = peewee.IntegerField()


class Post(Model):
    id = peewee.IntegerField()
    post_id = peewee.IntegerField()


database.connect()

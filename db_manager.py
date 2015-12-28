#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
import rethinkdb as rdb
from rethinkdb.errors import RqlRuntimeError, RqlDriverError


class DataBase(object):
    def __init__(self):
        self.RDB_HOST = 'zompigame.net'
        self.RDB_PORT = 28015
        self.DB_NAME = 'zompigame'
        self.TABLE_NAME = 'rating'
        self.auth_key = 'ZompKey69'
        self.connection = None

    def __get__(self):
        return self.connection

    def create_connection(self):
        try:
            self.connection = rdb.connect(host=self.RDB_HOST, port=self.RDB_PORT, db=self.DB_NAME, auth_key=self.auth_key)
            print('[*] Connection to DB Ok')
        except RqlDriverError:
            print(503, "No database connection could be established.")
            self.connection = None

    def close_connection(self):
        try:
            self.connection.close()
        except AttributeError:
            print(AttributeError)

    def insert(self, player_name, player_point, player_time, victims):
        print('[*] DB: Insert')
        rdb.db(self.DB_NAME).table(self.TABLE_NAME).insert([{'name': player_name,
                                                             'point': player_point,
                                                             'time': player_time,
                                                             'victims': victims}]).run(self.connection)

    def delete(self, player_name):
        print('[*] DB: Delete ' + player_name)
        rdb.db(self.DB_NAME).table(self.TABLE_NAME).get(player_name).delete().run(self.connection)

    def change(self, id, player_name, player_point, player_time, victims):
        print('[*] DB: Change ' + player_name)
        rdb.db(self.DB_NAME).table(self.TABLE_NAME).get(id).update({'name': player_name,
                                                                    'point': player_point,
                                                                    'time': player_time,
                                                                    'victims': victims}).run(self.connection)

    def count_by_name(self, player_name):
        print('[*] DB: Count by Name ' + player_name)
        cursor = rdb.db(self.DB_NAME).table(self.TABLE_NAME).filter(rdb.row["name"] == player_name).count().run(self.connection)
        return cursor

    def get_id_by_name(self, player_name):
        print('[*] DB: Get Id by Name "' + player_name + '"')
        cursor = rdb.db(self.DB_NAME).table(self.TABLE_NAME).filter(rdb.row["name"] == player_name).run(self.connection)
        for document in cursor:
            return document['id'], document['point']

    def make_full_insert(self, player_name, player_point, player_time, victims):
        if self.count_by_name(player_name) != 0:
            print('[*] DB: ' + player_name + ' Already in DB')
            id, point = self.get_id_by_name(player_name)
            if point < player_point:
                self.change(id, player_name, player_point, player_time, victims)
        else:
            self.insert(player_name, player_point, player_time, victims)

if __name__ == '__main__':
    db = DataBase()
    db.create_connection()
    if db.connection is not None:
        db.make_full_insert('thesystem69', 60, '10:0:0', 50)
        db.close_connection()

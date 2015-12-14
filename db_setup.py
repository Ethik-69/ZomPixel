#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
import rethinkdb as rdb
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
        
RDB_HOST = 'localhost'
RDB_PORT = 28015
DB_NAME = 'zompigame'
TABLE_NAME = 'rating'
auth_key = 'ZompKey69'


def setup():
    print('[*] DB Setup')
    connection = rdb.connect(host=RDB_HOST, port=RDB_PORT, auth_key=auth_key)
    try:
        rdb.db_create(DB_NAME).run(connection)
        rdb.db(DB_NAME).table_create(TABLE_NAME).run(connection)
        rdb.db(DB_NAME).table(TABLE_NAME).index_create('point').run(connection)
        #rdb.db('rethinkdb').table('cluster_config').get('auth').update({auth_key: 'ZompKey69'})
        print('Database setup completed')
    except RqlRuntimeError:
        print('App database already exists')
    finally:
        connection.close()
    print('[*] -Ok')

setup()

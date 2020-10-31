#! /usr/bin/python
# -*- coding:utf-8 -*-
import rethinkdb as rdb
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from zompixel.utils.log_config import LoggerManager

LOGGER = LoggerManager.getLogger("root")

RDB_HOST = "zompigame.net"
RDB_PORT = 28015
DB_NAME = "zompigame"
TABLE_NAME = "rating"
MAIL_TABLE_NAME = "mail"
auth_key = "ZompKey69"


def setup():
    LOGGER.info("[*] DB Setup")
    connection = rdb.connect(host=RDB_HOST, port=RDB_PORT, auth_key=auth_key)

    try:
        # rdb.db_create(DB_NAME).run(connection)
        rdb.db(DB_NAME).table_create(MAIL_TABLE_NAME).run(connection)
        # rdb.db(DB_NAME).table(TABLE_NAME).index_create('point').run(connection)
        # rdb.db('rethinkdb').table('cluster_config').get('auth').update({auth_key: 'ZompKey69'})
        LOGGER.info("Database setup completed")

    except RqlRuntimeError:
        LOGGER.info("App database already exists")

    except RqlDriverError as err:
        LOGGER.info(f"Database error: {err}")

    finally:
        connection.close()

    LOGGER.info("[*] -Ok")


setup()

import json
import sys
import sqlite3
import logging
from sqlite3 import Error

from flask import Flask, abort, jsonify, request

from init_db import DatabaseConnection

app = Flask(__name__)

FORMAT = '%(asctime)s|%(levelname)-15s|%(lineno)-8s|%(message)s'
logging.basicConfig(
        format=FORMAT,
        level=logging.DEBUG,
        stream=sys.stdout,
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
logger = logging.getLogger('__name__')


def get_database() -> DatabaseConnection:
    return DatabaseConnection(
        filename='identifier.sqlite', table='contacts')


def init_database() -> None:
    db = get_database()
    db.init_database()
    logger.debug(msg='DATABASE INITIALIZED')


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route('/simpleserver/api/contacts', methods=['GET', 'POST'])
def contacts():
    db = get_database()
    if request.method == 'GET':
        logger.debug(msg='DB CONNECTION SET')
        try:
            data = db.obtain()
            return json.dumps(data)
        except Error as err:
            logger.error(msg=err, exc_info=True)
            abort(404, description=err)
    else:
        data = request.json
        try:
            db.insert(data)
            message = dict(result='DATA SAVED')
            return [json.dumps(message)]
        except Error as err:
            logger.error(msg=err, exc_info=True)
            pass


def main():
    init_database()
    logger.debug(msg='STARTED')
    app.run()
    logger.debug(msg='FINISHED')


if __name__ == '__main__':
    main()



#!flask/bin/python
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager, Command
from flask.ext.migrate import MigrateCommand
from app import app, db, migrate, models


class CreateDb(Command):

    def run(self):
        print 'Creating the database.'
        db.create_all()

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('create_db', CreateDb())

if __name__ == '__main__':
    manager.run()

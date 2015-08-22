from steerclear import app, db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

"""
migrate
-------
Enable database creation/migration
taken from: https://flask-migrate.readthedocs.org/en/latest/
"""
def migrate():
    migrate = Migrate(app, db)

    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    manager.run()

if __name__ == '__main__':
    migrate()






from scuba_app import create_app
from config import DevConfig
from flask_migrate import MigrateCommand
from flask_script import Manager

app = create_app(DevConfig)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

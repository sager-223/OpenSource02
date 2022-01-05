from car_home import create_app,db
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask import render_template

app = create_app()

manager = Manager(app)

Migrate(app,db)

manager.add_command('db',MigrateCommand)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    manager.run()
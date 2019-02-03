from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from app.models import User

# Initializing the manager
manager = Manager(app)

# Initialize Flask Migrate
migrate = Migrate(app, db)

# Add the flask migrate
manager.add_command('db', MigrateCommand)

@manager.command
def dummy():
    # Create a user if they do not exist.
    user = User.query.filter_by(email="example@gmail.com").first()
    if not user:
        user = User("example@gmail.com", "123456")
        user.save()

# Run the manager
if __name__ == '__main__':
    manager.run()

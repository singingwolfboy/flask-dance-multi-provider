from flask import Flask
from .config import Config
from .models import db, bcrypt, login_manager
from .oauth import github_blueprint, google_blueprint
from .views import auth_blueprint, main_blueprint
from .cli import create_db, shell_context_processor


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(github_blueprint, url_prefix="/login")
    app.register_blueprint(google_blueprint, url_prefix="/login")
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.cli.add_command(create_db)
    app.shell_context_processors.append(shell_context_processor)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    return app

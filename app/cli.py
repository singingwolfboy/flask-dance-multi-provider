import click
from flask.cli import with_appcontext
from .models import db, User, OAuth


@click.command(name="createdb")
@with_appcontext
def create_db():
    db.create_all()
    db.session.commit()
    print("Database tables created")


def shell_context_processor():
    return {"db": db, "User": User, "OAuth": OAuth}

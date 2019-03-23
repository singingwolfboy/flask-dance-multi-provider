from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_bcrypt import Bcrypt
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm.collections import attribute_mapped_collection


db = SQLAlchemy()
bcrypt = Bcrypt()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    password_hash = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    @password.deleter
    def password(self):
        self.password_hash = None

    @property
    def has_password(self):
        return bool(self.password_hash)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class OAuth(OAuthConsumerMixin, db.Model):
    __table_args__ = (
        UniqueConstraint("provider", "provider_user_id"),
    )
    provider_user_id = db.Column(db.String(256))
    provider_user_login = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(
        User,
        # This `backref` thing sets up an `oauth` property on the User model,
        # which is a dictionary of OAuth models associated with that user,
        # where the dictionary key is the OAuth provider name.
        backref=db.backref(
            "oauth",
            collection_class=attribute_mapped_collection("provider"),
            cascade="all, delete-orphan",
        ),
    )



# setup login manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

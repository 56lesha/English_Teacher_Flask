from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from teacher import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(70), nullable=False)
    password_hash = db.Column(db.String(50), nullable=False)

    def check_password_correction(self, attempted_password):
        return self.password_hash == attempted_password

class Collection(db.Model):
    __tablename__ = "collection"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", foreign_keys="Collection.user_id", backref="collections")


class Words(db.Model):
    __tablename__ = "words"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String)
    translation = db.Column(db.String)
    collection_id = db.Column(db.Integer, ForeignKey("collection.id"), nullable=False)
    user = relationship("Collection", foreign_keys="Words.collection_id", backref="words")


















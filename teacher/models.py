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



class Words(db.Model):
    __tablename__ = "words"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String)
    translation = db.Column(db.String)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", foreign_keys="Words.user_id", backref="words")


















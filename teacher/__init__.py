from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///english_teacher.db"
app.config["SECRET_KEY"] = "6ee262feb841c981b32ffb412"
db = SQLAlchemy()
db.init_app(app)
login_manager = LoginManager(app)

from teacher import routes
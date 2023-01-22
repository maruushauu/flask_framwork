#  Пишем сценарий нашего приложения:
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))



SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)        # Экземпляр класса
migrate = Migrate(app, db)
login = LoginManager(app)  # экземпляр класса для авторизации пользователей
login.login_view = 'login'

from app import routes, models


# записываем второй импорт,чтобы избежать цикличности при составлении сценария
# setx export FLASK_APP=flask_app.py
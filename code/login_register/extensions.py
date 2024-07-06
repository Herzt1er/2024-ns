# extensions.py文件存在的意义：避免循环引用

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


db = SQLAlchemy()
mail = Mail()
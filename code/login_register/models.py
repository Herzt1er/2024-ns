from extensions import db
from datetime import datetime

# 需要把模型迁移到数据库
# 用户表 模型
class UserModel(db.Model):
    __tablename__ = "user"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True) # 邮箱必须唯一
    join_time = db.Column(db.DateTime, default=datetime.now)
    # 这里的datetime.now是一个函数，而datetime.now()是一个值

# 邮件验证码
class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(10), nullable=False)



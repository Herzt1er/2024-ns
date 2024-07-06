# 表单验证
from flask_wtf import FlaskForm
import wtforms
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Length, EqualTo, DataRequired
from models import UserModel, EmailCaptchaModel
from extensions import db
import re

# Form：主要就是用来验证前端提交的数据是否符合要求
class RegisterForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(message="邮箱不能为空"), Email(message="邮箱格式错误,请输入正确的邮箱")])
    captcha = StringField('验证码', validators=[DataRequired(), Length(min=6, max=6, message="验证码格式错误！")])
    username = StringField('用户名', validators=[DataRequired(message="用户名不能为空"), Length(min=3, max=10, message="用户名长度3~10位")])
    password = PasswordField('密码', validators=[DataRequired(message="密码不能为空"), Length(min=8, max=36, message="密码格式错误！")])
    password_confirm = PasswordField('确认密码', validators=[DataRequired(message="确认密码不能为空"), EqualTo("password", message="两次密码不一致！")])

    # 自定义验证：
    # 1. 邮箱是否已经被注册
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册！")

    # 2. 验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或验证码错误！")

    # 3. 验证用户名是否合法（是否存在非法字符）以及用户名是否被注册
    def validate_username(self, field):
        username = field.data
        print(username)
        # 检测到非法字符进入if
        if not re.search(u'^[a-zA-Z0-9\u4e00-\u9fa5]+$', username):
            msg = u"用户名不可以包含非法字符(!,@,#,$,%...)"
            print(msg)
            raise wtforms.ValidationError(message="用户名不可以包含非法字符")
        
        # 验证用户名是否已经被注册
        user = UserModel.query.filter_by(username=username).first()
        if user:
            raise wtforms.ValidationError(message="该用户名已经被注册！")

    # 4. 验证用户口令是否为弱口令
    def validate_password(self, field):
        password = field.data
        n = len(password)
        n1 = n2 = n3 = 0
        n1 = 0
        n2 = 0
        n3 = 0
        for i in range(0,n,1):
            ch = password[i]
            if "0"<=ch<="9":
                n1 = 1
            elif "a"<=ch<="z"or "A"<=ch<="Z":
                n2 = 1
            else:
                n3 = 1
        level = n1+n2+n3
        if level < 3:
            print("弱密码")
            raise wtforms.ValidationError(message="不可使用弱口令，请重新设置密码")


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message="用户名不能为空"), Length(min=3, max=10, message="用户名长度3~10位")])
    password = PasswordField('密码', validators=[DataRequired(message="密码不能为空"), Length(min=8, max=36, message="密码错误，长度为8-36字符")])
    
    # 验证用户名是否合法（是否存在非法字符）
    def validate_username(self, field):
        username = field.data
        print(username)
        # 检测到非法字符进入if
        if not re.search(u'^[a-zA-Z0-9\u4e00-\u9fa5]+$', username):
            msg = u"用户名不可以包含非法字符(!,@,#,$,%...)"
            print(msg)
            raise wtforms.ValidationError(message="用户名不可以包含非法字符")

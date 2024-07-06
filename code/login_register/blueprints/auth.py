from flask import Blueprint, render_template, jsonify, redirect, url_for, session, flash
from extensions import mail, db
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptchaModel
from .forms import RegisterForm, LoginForm
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash


# /auth
auth = Blueprint("auth", __name__, url_prefix="/auth")

# 登录
@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template("login.html", form=form)
    else:
        if form.validate():
            username = form.username.data
            password = form.password.data
            user = UserModel.query.filter_by(username=username).first()
            if not user:
                flash("用户名或密码错误", "danger")
                # print("用户在数据库中不存在！")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password, password):
                # cookie：
                # cookie中不适合存储太多的数据，只适合存储少量的数据
                # cookie一般用来存放登录授权的东西
                # flask中的session，是经过加密后存储在cookie中的
                session['user_id'] = user.id
                # print(session)
                # print(session['user_id'])
                # return "成功登录"
                return redirect(url_for('home.index'))
            else:
                flash("用户名或密码错误", "danger")
                print("密码错误！")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{getattr(form, field).label.text} - {error}", "danger")
            
        return render_template("login.html", form=form)

# 注册
@auth.route("/register", methods=['GET', 'POST'])
def register():
    # 验证用户提交的邮箱和验证码是否对应且正确
    # 表单验证：flask-wtf: wtforms
    form = RegisterForm(request.form)
    if request.method == 'GET':
        return render_template("register.html", form=form)
    else:
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            # 密码不能明文存储，在数据库表中使用generate_password_hash(password)生成hash值存储
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            # session['username'] = username
            db.session.add(user)
            db.session.commit()
            flash("注册成功！", "Success")
            return redirect(url_for("auth.login"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{getattr(form, field).label.text} - {error}", "danger")
            
        return render_template("register.html", form=form)

# 退出登录
@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# 获取邮箱验证码
# auth.route：如果没有指定methods参数，默认就是GET请求
@auth.route("/captcha/email")
def get_email_captcha():
    email = request.args.get("email")
    if email:
        source = string.digits * 6
        captcha = random.sample(source, 6)
        captcha = "".join(captcha)
        message = Message(subject="中传放心传-注册验证码", recipients=[email], body=f"您的验证码是:{captcha}")
        try:
            mail.send(message)
            email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(email_captcha)
            db.session.commit()
            return jsonify({"code": 200, "message": "Email sent successfully!", "data": None})
        except Exception as e:
            print(f"Error sending email: {e}")  # 添加日志信息
            return jsonify({'error': str(e)}), 500    
    return jsonify({'error': 'Email is required'}), 400
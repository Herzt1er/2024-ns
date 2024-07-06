# app与其他蓝图建立关联，则不再用来编写视图函数

from flask import Flask, session, g
# 导入config配置文件
import config 
# 导入db，与extensions.py产生关联，其他同理
from extensions import db, mail
from models import UserModel
from blueprints.auth import auth as auth_bp
from blueprints.home import home as home_bp
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect


# 创建app对象
app = Flask(__name__)
CSRFProtect(app)

#绑定配置文件
app.config.from_object(config)

# 先创建db对象（在extensions.py中），再进行app对象的绑定
db.init_app(app)
mail.init_app(app)

# 数据库迁移
migrate = Migrate(app, db)

# 绑定bp
app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)


@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


@app.context_processor
def my_context_processor():
    return {"user": g.user}


if __name__=='__main__':
    app.debug = True
    app.run()
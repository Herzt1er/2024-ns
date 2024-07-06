# 用来做一些配置
import os

# 使用Flask-WTF需要配置参数SECRET_KEY，form.py表单验证
# SECRET_KEY用来建立加密的令牌，用于验证Form表单提交，可以设置的复杂些防止被恶意破解
SECRET_KEY = os.urandom(24)
CSRF_ENABLED = True

# 先创建“中传放心传”数据库
HOSTNAME = '127.0.0.1'
PORT='3306'
DATABASE = 'cesdb' # Cainiao E Station database的缩写
USERNAME = 'root' # 用户名
PASSWORD = '123' # 数据库密码
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "muttonbuns@qq.com"
MAIL_PASSWORD = ""
MAIL_DEFAULT_SENDER = "muttonbuns@qq.com"














# 环境搭建步骤

## Kali-Linux-2024.1 搭建步骤

### 1、更新apt源，安装相关依赖包

```shell
sudo apt update
sudo apt install python3
pip3 install pipenv
```

### 2、启动 mysql 服务

```shell
sudo systemctl status mysql
sudo systemctl start mysql

mysql -u root -p # 进入 mysql
MariaDB [(none)]> create database cesdb; # 创建数据库 cesdb
MariaDB [(none)]> create user 'your_name'@localhost identified by 'your_password'; #（可选）创建一个用户来管理该数据库，可以跳过这步直接使用root用户
MariaDB [(none)]> grant all privileges on cesdb.* to 'your_name'@localhost; # （可选）同上，如果创建新用户，需要给予该用户cesdb的数据库权限
MariaDB [(none)]> flush privileges; # 刷新使得配置生效
```

### 3、config.py 文件配置说明

```shell
# 先创建“中传放心传”数据库
HOSTNAME = '127.0.0.1'
PORT='3306'
DATABASE = 'cesdb' # Cainiao E Station database的缩写
USERNAME = 'root' # 用户名，如果新创建了其他用户，则需要修改此处的用户名+数据库密码
PASSWORD = '123' # 数据库密码
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "muttonbuns@qq.com"
MAIL_PASSWORD = "" # 邮箱授权码（考虑到安全性，此处省略，具体的授权码会在讨论群给出，请勿外传！！！）
MAIL_DEFAULT_SENDER = "muttonbuns@qq.com"
```

### 4、代码环境配置

```shell
# 将该项目代码复制到Kali虚拟机中
cd login_register # 进入代码所在目录
pipenv shell # 进入pipenv环境
pipenv install # 安装pipenv环境所需要的依赖包
pipenv run pip list # 检查已安装的包列表

# 初始化数据库
pipenv run flask db init
pipenv run flask db migrate -m "Initial migration." 
pipenv run flask db upgrade
```

### 5、在pipenv环境中运行Flask应用

```shell
pipenv run flask run # 在虚拟机中可以访问
pipenv run flask run --host=0.0.0.0 # 如果从其他设备（如宿主机）访问Flask应用，需要让Flask监听所有IP地址
```

### 6、访问页面

```shell
http://127.0.0.1:5000
```

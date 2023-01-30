SECRET_KEY="jkdghksgfgfgcfcfhfg"
# mysql所在的主机名
HOSTNAME = "127.0.0.1"
# mysql监听的端口号
PORT = 3306
# 数据库名称
DATABASE = "race"
# 连接mysql的用户名
USERNAME = "root"
# 连接密码
PASSWORD = "123456"
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

#配置邮箱
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "2351715714@qq.com"
MAIL_PASSWORD = ""
MAIL_DEFAULT_SENDER = "2351715714@qq.com"



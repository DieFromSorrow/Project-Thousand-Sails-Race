
import os

SECRET_KEY = "secret_key"

# mysql所在的主机名
HOSTNAME = "127.0.0.1"
# mysql监听的端口号
PORT = 3306
# 数据库名称
DATABASE = "race"
# 连接mysql的用户名
USERNAME = os.getenv('DATABASE_USERNAME')
# 连接密码
PASSWORD = os.getenv('DATABASE_PASSWORD')
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# 配置邮箱
'''
MAIL_SERVER = "smtp.sendgrid.net"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = '2937128647@qq.com'
MAIL_PASSWORD = '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'
# MAIL_PASSWORD = os.getenv('SENDGRID_API_KEY')
MAIL_DEFAULT_SENDER = ('Thousand_Sails_Race_Admin', '2937128647@qq.com')
'''

MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = os.getenv('QQ_ACCOUNT')
MAIL_PASSWORD = os.getenv('QQMAIL_API_KEY')
# MAIL_PASSWORD = os.getenv('SENDGRID_API_KEY')
MAIL_DEFAULT_SENDER = ('Thousand_Sails_Race_Admin', MAIL_USERNAME)


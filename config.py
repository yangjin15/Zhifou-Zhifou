SECRET_KEY = "asdkjfoaimlskdjfs;ld"

HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "root"
DATABASE = "qa"
DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_DATABASE_URI = DB_URI

# Email configuration
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "3273759790@qq.com"
MAIL_PASSWORD = "dtflrpntjjpychcd"
MAIL_DEFAULT_SENDER = "3273759790@qq.com"

# File upload configuration
UPLOAD_FOLDER = 'static/user_images'  # 上传文件夹路径

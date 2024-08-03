import secrets
import os

# Flask应用的名称

APP_NAME = "myblog"

# Flask应用的版本
APP_VERSION = "1.0.0"

# 应用文件的根路径
APP_ROOT_PATH = "."

# Flask应用的主机名或IP地址
APP_HOST = '127.0.0.1'  # (str)

# Flask应用的端口号
APP_PORT = 5000

# 切换Flask应用的调试模式
DEBUG_MODE = True

# 模板文件夹的路径
TEMPLATE_FOLDER = f"templates"

# 静态文件夹的路径
STATIC_FOLDER = f"static"

# 用户头像
USER_PROFILE_PICTURE = f"https://api.dicebear.com/9.x/bottts/svg?seed="

# 头像大小
RADIUS_PROFILE_PICTURE = "&radius=10"

DAILY_QUOTES_URL = "https://apiv3.shanbay.com/weapps/dailyquote/quote"

### 日志设置 ###
# 切换自定义日志功能
CUSTOM_LOGGER = True

# 切换werkzeug日志功能
WERKZEUG_LOGGER = False

# 日志文件夹的根路径
LOG_FOLDER_ROOT = 'database/log/'

# 日志文件的根路径
LOG_FILE_ROOT = LOG_FOLDER_ROOT + "log.log"

# 危险日志文件的根路径
LOG_DANGER_FILE_ROOT = LOG_FOLDER_ROOT + "logDanger.log"

# 成功日志文件的根路径
LOG_SUCCESS_FILE_ROOT = LOG_FOLDER_ROOT + "logSuccess.log"

# 警告日志文件的根路径
LOG_WARNING_FILE_ROOT = LOG_FOLDER_ROOT + "logWarning.log"

# 信息日志文件的根路径
LOG_INFO_FILE_ROOT = LOG_FOLDER_ROOT + "logInfo.log"

# 应用日志文件的根路径
LOG_APP_FILE_ROOT = LOG_FOLDER_ROOT + "logApp.log"

# SQL日志文件的根路径
LOG_SQL_FILE_ROOT = LOG_FOLDER_ROOT + "logSQL.log"

# Flask会话的秘密密钥
APP_SECRET_KEY = secrets.token_urlsafe(32)

# 切换Flask应用的永久会话
SESSION_PERMANENT = True

# 日志文件中使用的分隔符文本
BREAKER_TEXT = "\n"

### 数据库设置 ###

# 数据库文件夹的根路径
DB_FOLDER_ROOT = 'database/db/'

# 用户数据库的根路径
DB_USERS_ROOT = DB_FOLDER_ROOT + "users.db"

# 帖子数据库的根路径
DB_POSTS_ROOT = DB_FOLDER_ROOT + "posts.db"

# 评论数据库的根路径
DB_COMMENTS_ROOT = DB_FOLDER_ROOT + "comments.db"

### SMTP邮件设置 ###

# SMTP服务器地址
SMTP_SERVER = "smtp.qq.com"

# SMTP server port
SMTP_PORT = 587

# SMTP mail address
SMTP_MAIL = os.environ.get("SMTP_MAIL", "zhl")

# SMTP mail password
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "zhl")

### 默认管理员账户设置 ###

# 切换创建默认管理员账户
DEFAULT_ADMIN = True

# 默认管理员用户名
DEFAULT_ADMIN_USERNAME = "zhl"

# 默认管理员电子邮件地址
DEFAULT_ADMIN_EMAIL = os.environ.get("DEFAULT_ADMIN_EMAIL", "zhl")

# 默认管理员密码
DEFAULT_ADMIN_PASSWORD = os.environ.get("DEFAULT_ADMIN_PASSWORD", "zhl")

# 管理员的默认起始积分
DEFAULT_ADMIN_POINT = 0

# 默认管理员的个人资料图片URL
DEFAULT_ADMIN_PROFILE_PICTURE = USER_PROFILE_PICTURE + DEFAULT_ADMIN_USERNAME + RADIUS_PROFILE_PICTURE

### RECAPTCHA设置 ###

RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY", "6LeXYRgqAAAAAF4HUOV5nuaEvWO8e465mBb5PUas")  # (str)

RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY", "6LeXYRgqAAAAACLGvLsDa1ebYurJR4XXeeK_PS10")  # (str)

RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"  # (str)

# 切换不同操作的reCAPTCHA验证
RECAPTCHA_LOGIN = True
RECAPTCHA_SIGN_UP = True
RECAPTCHA_POST_CREATE = True
RECAPTCHA_POST_EDIT = True
RECAPTCHA_POST_DELETE = True
RECAPTCHA_COMMENT = True
RECAPTCHA_COMMENT_DELETE = True
RECAPTCHA_PASSWORD_RESET = True
RECAPTCHA_PASSWORD_CHANGE = True
RECAPTCHA_USERNAME_CHANGE = True
RECAPTCHA_VERIFY_USER = True
RECAPTCHA_DELETE_USER = True
RECAPTCHA_PROFILE_PICTURE_CHANGE = True

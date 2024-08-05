import secrets
import os

# Flask应用的名称

APP_NAME = "myblog"

# Flask应用的版本
APP_VERSION = "1.0.0"

# 应用文件的根路径
APP_ROOT_PATH = "."

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
CUSTOM_LOGGER = False

# 切换werkzeug日志功能
WERKZEUG_LOGGER = False

# Flask会话的秘密密钥
APP_SECRET_KEY = secrets.token_urlsafe(32)

# 切换Flask应用的永久会话
SESSION_PERMANENT = True

# 日志文件中使用的分隔符文本
BREAKER_TEXT = "\n"

### SMTP邮件设置 ###

# SMTP服务器地址
SMTP_SERVER = "smtp.qq.com"

# SMTP server port
SMTP_PORT = 587

# SMTP mail address
SMTP_MAIL = os.environ.get("SMTP_MAIL", "")

# SMTP mail password
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")


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

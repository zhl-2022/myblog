import secrets
import os
APP_NAME = "myblog"
APP_VERSION = "1.0.0"
APP_ROOT_PATH = "."
TEMPLATE_FOLDER = f"templates"
STATIC_FOLDER = f"static"
USER_PROFILE_PICTURE = f"https://api.dicebear.com/9.x/bottts/svg?seed="
RADIUS_PROFILE_PICTURE = "&radius=10"
DAILY_QUOTES_URL = "https://apiv3.shanbay.com/weapps/dailyquote/quote"
CUSTOM_LOGGER = False
WERKZEUG_LOGGER = False
APP_SECRET_KEY = secrets.token_urlsafe(32)
SESSION_PERMANENT = True
BREAKER_TEXT = "\n"
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587

# SMTP mail address
SMTP_MAIL = os.environ.get("SMTP_MAIL", "")

# SMTP mail password
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")


### RECAPTCHA设置 ###

RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY", "6LeXYRgqAAAAAF4HUOV5nuaEvWO8e465mBb5PUas")  # (str)

RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY", "6LeXYRgqAAAAACLGvLsDa1ebYurJR4XXeeK_PS10")  # (str)

RECAPTCHA_VERIFY_URL = "https://recaptcha.net/recaptcha/api/siteverify"
# https://www.google.com/recaptcha/api/siteverify"  # (str)

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

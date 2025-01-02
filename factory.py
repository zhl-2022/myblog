# -*- coding: utf-8 -*-
"""
File:       factory.py
Time:       2024-07-28-23:23
User:       zhl
Details:       
"""
# -*- coding: utf-8 -*-
"""
File:       factory.py
Time:       2024-07-28-23:23
User:       zhl
Details:       
"""
from flask import Flask
from flask_wtf.csrf import CSRFError, CSRFProtect
from utils import notFoundErrorHandler, unauthorizedErrorHandler, csrfErrorHandler, internalErrorHandler, currentDate
from flask_caching import Cache
from constants import *
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from utils import *
from datetime import timedelta
from routes.blog import blogBlueprint
from routes.contact import contactBlueprint
from routes.single_blog import single_blogBlueprint
from routes.verifyUser import verifyUserBlueprint
from routes.add import addBlueprint
from routes.edit import editBlueprint
from pymongo import MongoClient


def get_seconds_until_midnight():
    """获取当前时间到次日凌晨的秒数"""
    now = datetime.now()
    midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0)
    return int((midnight - now).total_seconds())


app = Flask(import_name=APP_NAME, root_path=APP_ROOT_PATH, static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)
URL = os.environ.get("URL", "")
client = MongoClient(URL)
app.mongo_db = client['myblog']

app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 3000
cache = Cache(app)
app.secret_key = APP_SECRET_KEY
app.config["SESSION_PERMANENT"] = (SESSION_PERMANENT)
app.register_blueprint(blogBlueprint)
app.register_blueprint(contactBlueprint)
app.register_blueprint(verifyUserBlueprint)
app.register_blueprint(single_blogBlueprint)
app.register_blueprint(addBlueprint)
app.register_blueprint(editBlueprint)
app.register_blueprint(indexBlueprint)


@cache.memoize(timeout=get_seconds_until_midnight())  # 缓存结果直到次日凌晨
def get_daily_quote():
    response = requests.get(DAILY_QUOTES_URL)
    if response.status_code == 200:
        quote = response.json()
        cached_data = dict(translation=quote['translation'], content=quote['content'], share_img_urls=quote['share_img_urls'], date=currentDate())
        cache.set("get_daily_quote", cached_data)  # 手动设置缓存
        print(f"Cache hit for get_daily_quote {cached_data}")
        return cached_data
    else:
        print(f"get_daily_quote failed with {response.status_code}")
        return dict(translation="程序错误中，80% 是语法错误，16% 是简单的逻辑错误，0.8% 才是困难的问题。", content="代码写得越急，程序跑得越慢。", share_img_urls=[], date=currentDate())


@cache.memoize(timeout=get_seconds_until_midnight())  # 缓存结果直到次日凌晨
def getProfilePicture(userName):
    if not userName:
        return None

    # 假设你的 MongoDB 集合名为 users
    user_document = app.mongo_db['users'].find_one({"userName": userName})
    if user_document:
        profilePicture = user_document.get("profilePicture")
        print(f"Cache hit for getProfilePicture {userName}")
        return profilePicture
    else:
        print(f"User {userName} not found or profile picture missing.")
        return None


scheduler = BackgroundScheduler()
scheduler.add_job(func=get_daily_quote, trigger="cron", hour=0, minute=0)
scheduler.start()

csrf = CSRFProtect(app)


@app.errorhandler(404)
def notFound(e):
    return notFoundErrorHandler(e)


@app.errorhandler(401)
def unauthorized(e):
    return unauthorizedErrorHandler(e)


@app.errorhandler(500)
def internalerror(e):
    return internalErrorHandler(e)


@app.errorhandler(CSRFError)
def csrfError(e):
    return csrfErrorHandler(e)


# @app.after_request
# def afterRequest(response):
#     return afterRequestLogger(response)


@app.context_processor
def inject_variables():
    cached_quote = cache.get("get_daily_quote")
    if not cached_quote:
        cached_quote = get_daily_quote()
    return {'getProfilePicture': getProfilePicture, 'get_daily_quote': cached_quote}


def create_app():
    return app

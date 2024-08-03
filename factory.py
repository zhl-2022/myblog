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
from flask import Flask, g
import sqlite3
from utils.log import Log
from flask_wtf.csrf import CSRFError, CSRFProtect
from utils import notFoundErrorHandler, unauthorizedErrorHandler, csrfErrorHandler, afterRequestLogger, internalErrorHandler, currentDate
from flask_caching import Cache
from constants import *
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import os

log = Log()

print("templates/blog.html", os.path.abspath('templates/blog.html'))


# def check_and_delete_logs():
#     log_files = [LOG_FILE_ROOT, LOG_DANGER_FILE_ROOT, LOG_SUCCESS_FILE_ROOT, LOG_WARNING_FILE_ROOT, LOG_INFO_FILE_ROOT, LOG_APP_FILE_ROOT, LOG_SQL_FILE_ROOT]
#     log.check_and_delete_logs(log_files)


def get_db1():
    """posts"""
    if 'db1' not in g:
        g.db1 = sqlite3.connect(DB_POSTS_ROOT)
        g.db1.set_trace_callback(Log.sql)
    return g.db1


def get_db2():
    """user"""
    if 'db2' not in g:
        g.db2 = sqlite3.connect(DB_USERS_ROOT)
        g.db2.set_trace_callback(Log.sql)
    return g.db2


def get_db3():
    """comment"""
    if 'db3' not in g:
        g.db3 = sqlite3.connect(DB_COMMENTS_ROOT)
        g.db3.set_trace_callback(Log.sql)
    return g.db3


def get_seconds_until_midnight():
    """获取当前时间到次日凌晨的秒数"""
    now = datetime.now()
    midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0)
    return int((midnight - now).total_seconds())


app = Flask(
    import_name=APP_NAME,  # The name of the app
    root_path=APP_ROOT_PATH,  # The root path of the app
    static_folder=STATIC_FOLDER,  # The folder where the static files(*.js/*.css) are stored
    template_folder=TEMPLATE_FOLDER,  # The folder where the Jinja(*.html.jinja) templates are stored
)
app.config['CACHE_TYPE'] = 'SimpleCache'  # 或其他缓存类型
app.config['CACHE_DEFAULT_TIMEOUT'] = 3000  # 设置默认超时时间
cache = Cache(app)

app.secret_key = APP_SECRET_KEY
app.config["SESSION_PERMANENT"] = (SESSION_PERMANENT)


@cache.memoize(timeout=get_seconds_until_midnight())  # 缓存结果直到次日凌晨
def get_daily_quote():
    response = requests.get(DAILY_QUOTES_URL)
    if response.status_code == 200:
        quote = response.json()
        cached_data = dict(translation=quote['translation'], content=quote['content'], share_img_urls=quote['share_img_urls'], date=currentDate())
        cache.set("get_daily_quote", cached_data)  # 手动设置缓存
        Log.info(f"Cache hit for get_daily_quote {cached_data}")
        return cached_data
    else:
        Log.danger(f"get_daily_quote failed with {response.status_code}")
        return dict(translation="程序错误中，80% 是语法错误，16% 是简单的逻辑错误，0.8% 才是困难的问题。", content="代码写得越急，程序跑得越慢。", share_img_urls=[], date=currentDate())


@cache.memoize(timeout=get_seconds_until_midnight())  # 缓存结果直到次日凌晨
def getProfilePicture(userName):
    if not userName:
        return None
    db_user = get_db2()
    cursor_user = db_user.cursor()
    try:
        cursor_user.execute("""select profilePicture from users where userName = ? """, (userName,))
        profilePicture = cursor_user.fetchone()[0]
        Log.info(f"Cache hit for getProfilePicture {userName}")
        return profilePicture
    except Exception as e:
        Log.danger(f"Error fetching profile picture for {userName}: {e}")
        return None


# 设置定时任务，每天更新一次
scheduler = BackgroundScheduler()
scheduler.add_job(func=get_daily_quote, trigger="cron", hour=0, minute=0)
# scheduler.add_job(func=check_and_delete_logs, trigger="cron", hour=0, minute=0)
scheduler.start()

csrf = CSRFProtect(app)


@app.teardown_appcontext
def close_db(e=None):
    db1 = g.pop('db1', None)
    if db1 is not None:
        db1.close()

    db2 = g.pop('db2', None)
    if db2 is not None:
        db2.close()

    db3 = g.pop('db3', None)
    if db3 is not None:
        db3.close()


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


@app.after_request
def afterRequest(response):
    return afterRequestLogger(response)


@app.context_processor
def inject_variables():
    cached_quote = cache.get("get_daily_quote")
    if not cached_quote:
        cached_quote = get_daily_quote()
        Log.danger("没有使用缓存")

    return {'getProfilePicture': getProfilePicture, 'get_daily_quote': cached_quote}


def create_app():
    return app

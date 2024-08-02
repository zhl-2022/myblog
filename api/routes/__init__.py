from ..utils import Log
from ..constants import *
from flask import abort, flash
from requests import post as requestsPost
from ..factory import get_db2, get_db1, get_db3
import requests
import json
import time


def markdown_to_html(md_content, max_retries=3, delay=2):
    url = 'https://api.github.com/markdown'
    headers = {'Content-Type': 'application/json'}
    data = {
        'text': md_content,
        'mode': 'markdown'  # 使用标准的Markdown模式
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # 检查请求是否成功
            return response.text
        except requests.exceptions.RequestException as e:
            Log.danger(f"请求失败: https://api.github.com/markdown {e}")
            if attempt < max_retries - 1:
                Log.info(f"等待 {delay} 秒后重试...")
                time.sleep(delay)
            else:
                Log.danger("已达到最大重试次数，转换失败。")
                return None


def verify_recaptcha(secretResponse):
    if not secretResponse:
        Log.danger(f"User Verify reCAPTCHA Error")
        abort(401)
    verifyResponse = requestsPost(url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}").json()
    if not verifyResponse.get("success") and verifyResponse.get("score", 0.0) < 0.5:
        Log.danger(f"User Verify reCAPTCHA | verification: {verifyResponse.get('success')} | verification score: {verifyResponse.get('score')}")
        abort(401)


def verify_form(form):
    if not form.validate():
        for field, errors in form.errors.items():
            for error in errors:
                if field == "postBanner":
                    continue
                Log.danger(f"{field}: {error}")
                flash(f'Error in {field}: {error}', 'error')


def addPoints(points, user):
    db_user = get_db2()
    cursor_user = db_user.cursor()
    cursor_user.execute("""update users set points = points+? where userName = ? """, ((points), (user)))  # 这里需要检查是否存在用户
    db_user.commit()


class Delete:
    def post(postID):
        db_post = get_db1
        cursor_post = db_post.cursor()
        cursor_post.execute("""select author from posts where id = ? """, (postID,))
        cursor_post.execute("""delete from posts where id = ? """, (postID,))
        cursor_post.execute("update sqlite_sequence set seq = seq-1")
        db_post.commit()
        db_comment = get_db3
        cursor_comment = db_comment.cursor()
        cursor_comment.execute("""select count(*) from comments where post = ? """, (postID,))
        commentCount = list(cursor_comment)[0][0]
        cursor_comment.execute("""delete from comments where post = ? """, (postID,))
        cursor_comment.execute("""update sqlite_sequence set seq = seq - ? """, (commentCount,))
        db_comment.commit()
        flash(f"Post: {postID} deleted.", "error")
        Log.success(f'Post: "{postID}" deleted')

    def user(userName):
        db_user = get_db2
        cursor_user = db_user.cursor()
        cursor_user.execute("""delete from users where userName = ? """, (userName,))
        cursor_user.execute("update sqlite_sequence set seq = seq-1")
        db_user.commit()
        flash(f"User: {userName} deleted.", "error")
        Log.success(f'User: "{userName}" deleted')

    def comment(commentID):
        db_comment = get_db3
        cursor_comment = db_comment.cursor()
        cursor_comment.execute("""select user from comments where id = ? """, (commentID,))
        cursor_comment.execute("""delete from comments where id = ? """, (commentID,))
        cursor_comment.execute("update sqlite_sequence set seq = seq-1")
        db_comment.commit()
        flash(f"Comment: {commentID} deleted.", "error")
        Log.success(f'Comment: "{commentID}" deleted')

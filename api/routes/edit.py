from ..utils import *
from flask import render_template, flash, session, request, redirect, Blueprint, url_for
from ..constants import *
from . import verify_recaptcha, addPoints
from ..factory import get_db2, get_db1, get_db3
import base64

editBlueprint = Blueprint("edit", __name__)


@editBlueprint.route("/edit/<int:postID>", methods=["GET", "POST"])
def edit(postID):
    if session.get("role") != 'admin':
        flash(f"You are not logged in Or not an administrator Sorry!", "error")
        return redirect("/contact")
    db_post = get_db1()
    cursor_post = db_post.cursor()
    cursor_post.execute("SELECT * FROM posts WHERE id= ?", (postID,))
    post = cursor_post.fetchone()
    if post[5] != session["userName"]:
        flash("This post is not yours.", "error")
        Log.danger(f'User: "{session["userName"]}" tried to edit another authors post')
        return redirect(f"/single_blog/{postID}")
    title, tag, content, banner, category, views, timeStamp, lastEditTimeStamp = post[1], post[2], post[3], post[4], post[9], post[6], post[7], post[8]
    image = base64.b64encode(banner).decode('utf-8')
    db_comment = get_db3()
    cursor_comment = db_comment.cursor()
    cursor_comment.execute("""select count(*) from comments where post = ?""", (postID,))
    comments_nums = cursor_comment.fetchone()[0]
    if request.method == "POST":
        verify_recaptcha(request.form.get("g-recaptcha-response"))
        update_fields = ["lastEditTimeStamp  = ?"]
        params = [currentTime()]
        old_fields = [title, tag, banner, category]
        new_fields = [request.form["postTitle"], request.form["postTags"], request.files["postBanner"].read(), request.form["postCategory"]]
        for i in range(4):
            if new_fields[i]:
                update_fields.append(f"{old_fields[i]} = ?")
                params.append(new_fields[i])
        if request.form["postContent"] != content:
            update_fields.append("content  = ?")
            params.append(request.form["postContent"])
        # 添加id参数
        params.append(post[0])

        # 构建完整的SQL语句
        sql = f"UPDATE posts SET {', '.join(update_fields)} WHERE id = ?"

        # 执行SQL语句
        cursor_post.execute(sql, params)
        db_post.commit()
        addPoints(20, session["userName"])
        flash("You earned 20 points by edit post.", "success")
        Log.success(f'Post: "{request.form["postTitle"]}" edited', )
        return redirect(url_for("single_blog.single_blog", postID=postID))
    else:
        return render_template("edit.html", siteKey=RECAPTCHA_SITE_KEY, title=title, image=image, comments_nums=comments_nums,
                               tag=tag, content=content, category=category, views=views, timeStamp=timeStamp, lastEditTimeStamp=lastEditTimeStamp)

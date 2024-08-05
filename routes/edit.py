from flask import render_template, flash, session, request, redirect, Blueprint, url_for, current_app
from constants import *
from routes import verify_recaptcha
import base64
from bson import Binary, ObjectId
from utils import currentTime

editBlueprint = Blueprint("edit", __name__)


@editBlueprint.route("/edit/<string:postID>", methods=["GET", "POST"])
def edit(postID):
    if not session.get("isVerified"):
        flash(f"You are not logged in Or not Verified, Sorry!", "error")
        return redirect("/contact")
    # 获取MongoDB集合
    posts_collection = current_app.mongo_db['posts']
    # 查询特定的帖子
    post = posts_collection.find_one({"_id": ObjectId(postID)})
    if post["author"] != session["userName"]:
        flash("This post is not yours.", "error")
    title, tags, content, image, category, views, timeStamp, lastEditTimeStamp = post["title"], post["tags"], post["content"], base64.b64encode(post["banner"]).decode('utf-8'), post["category"], post["views"], post["timeStamp"], post["lastEditTimeStamp"]
    comments_collection = current_app.mongo_db['comments']
    # 计算特定帖子的评论数量
    comments_nums = comments_collection.count_documents({"post": ObjectId(postID)})
    if request.method == "POST":
        verify_recaptcha(request.form.get("g-recaptcha-response"))
        # 获取MongoDB集合
        # 构建更新字段
        update_fields = {"lastEditTimeStamp": currentTime()}
        old_fields = ["title", "tags", "banner", "category"]
        new_fields = [request.form["postTitle"], request.form["postTags"], request.files["postBanner"].read() if request.files.get("postBanner") else None, request.form["postCategory"]]
        for i in range(4):
            if new_fields[i]:
                update_fields[old_fields[i]] = new_fields[i]

        if request.form["postContent"] != content:
            update_fields["content"] = request.form["postContent"]
        # 执行更新操作
        posts_collection.update_one({"_id": ObjectId(postID)}, {"$set": update_fields})
        flash("You earned 20 points by edit post.", "success")
        return redirect(url_for("single_blog.single_blog", postID=postID))
    else:
        return render_template("edit.html", siteKey=RECAPTCHA_SITE_KEY, title=title, image=image, comments_nums=comments_nums,
                               tags=tags, content=content, category=category, views=views, timeStamp=timeStamp, lastEditTimeStamp=lastEditTimeStamp)

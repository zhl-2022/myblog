import base64
import smtplib
import ssl
from utils import *
from flask import render_template, flash, session, request, redirect, Blueprint, current_app
from constants import *
from email.message import EmailMessage
from routes import verify_recaptcha, verify_form, markdown_to_html
from bson import ObjectId
single_blogBlueprint = Blueprint("single_blog", __name__)


@single_blogBlueprint.route("/single_blog/<string:postID>", methods=["GET", "POST"])
def single_blog(postID):
    posts_collection = current_app.mongo_db['posts']
    comments_collection = current_app.mongo_db['comments']
    users_collection = current_app.mongo_db['users']

    # 查询特定的帖子
    post = posts_collection.find_one({"_id": ObjectId(postID)})
    if post:
        # 更新浏览次数
        posts_collection.update_one({"_id": ObjectId(postID)}, {"$inc": {"views": 1}})

        if request.method == "POST":
            if not session.get("userName"):
                flash(f"You are not logged in", "error")
                return redirect("/contact")
            verify_recaptcha(request.form.get("g-recaptcha-response"))
            verify_form(CommentForm(request.form))
            comment = request.form["comment"]
            parent_id = request.form.get("parent_id")
            to_email = post["author"]
            if parent_id:
                parent_comment = comments_collection.find_one({"id": parent_id})
                parent_user = parent_comment["user"]
                to_email = parent_user
                comments_collection.insert_one({
                    "post":postID,
                    "comment": comment,
                    "user": session["userName"],
                    "parent_id": parent_id,
                    "parent_user": parent_user,
                    "timeStamp": currentTime()
                })
            else:
                comments_collection.insert_one({
                    "post": postID,
                    "comment": comment,
                    "user": session["userName"],
                    "timeStamp": currentTime()
                })
            flash("You earned 5 points by commenting.", "success")
            user = users_collection.find_one({"userName": to_email})
            email = user["email"]
            context = ssl.create_default_context()
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(SMTP_MAIL, SMTP_PASSWORD)
            mail = EmailMessage()
            mail.set_content(f"Hi 👋,\n {session['userName']} had give you a comment on {post['title']} ")
            mail.add_alternative(
                f"""\
                <html>
                <body>
                    <div style="font-family: Arial, sans-serif;  max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius:0.5rem;">
                    <div style="text-align: center;">
                        <p style="font-size: 20px;">
                        点击 <a href="https://zhl2022.chat/single_blog/{postID}"> 这里 </a> 进行访问.
                        </p>
                    </div>
                    </div>
                </body>
                </html>
            """,
                subtype="html")
            mail["Subject"] = (f"👋🏻 {session['userName']} commented on your blog {post['title']}")
            mail["From"] = SMTP_MAIL
            mail["To"] = email
            try:
                server.send_message(mail)
            except Exception as e:
                flash(f"Comment to {parent_user} Incorrect email {e}", "error")
            server.quit()

        # 查询特定帖子的评论
        comments = list(comments_collection.find({"post": postID}).sort("timeStamp", -1))

        # 查询所有分类
        categories = list(posts_collection.aggregate([
            {"$group": {"_id": "$category", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]))

        # 查询最近的帖子
        recent_posts = list(posts_collection.find({}, {"id": 1, "title": 1, "banner": 1, "lastEditTimeStamp": 1, "category": 1, "author": 1}).sort("lastEditTimeStamp", -1).limit(3))
        for recent_post in recent_posts:
            recent_post['_id'] = str(recent_post['_id'])
            recent_post['banner'] = base64.b64encode(recent_post['banner']).decode('utf-8')

        content = markdown_to_html(post["content"])
        return render_template("single_blog.html", postid=postID, title=post["title"], tags=post["tags"].split(','), content=content, author=post["author"], image=base64.b64encode(post["banner"]).decode('utf-8'), views=post["views"],
                               timeStamp=post["timeStamp"], lastEditTimeStamp=post["lastEditTimeStamp"],
                               comments=comments, categories=categories, enumerate=enumerate, recent_posts=recent_posts, comments_nums=len(comments), siteKey=RECAPTCHA_SITE_KEY)
    else:
        flash(f"This {postID} blog cannot be found", "error")
        return redirect("/")

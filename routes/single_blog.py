import base64
from factory import get_db1, get_db3, get_db2

import smtplib
import ssl
from utils import *
from flask import render_template, flash, session, request, redirect, Blueprint, url_for
from constants import *
from email.message import EmailMessage
from routes import verify_recaptcha, verify_form, Delete, addPoints, markdown_to_html

single_blogBlueprint = Blueprint("single_blog", __name__)


@single_blogBlueprint.route("/single_blog/<int:postID>", methods=["GET", "POST"])
def single_blog(postID):
    db_post = get_db1()
    cursor_post = db_post.cursor()
    db_comment = get_db3()
    cursor_comment = db_comment.cursor()
    db_user = get_db2()
    cursor_user = db_user.cursor()

    cursor_post.execute("""select * from posts where id = ? """, (postID,))
    post = cursor_post.fetchone()
    if post:
        cursor_post.execute("""update posts set views = views+1 where id = ? """, (postID,))
        db_post.commit()
        if request.method == "POST":
            # if "postDeleteButton" in request.form:
            #     Delete.post(postID)
            #     return redirect(f"/blog")
            # if "commentDeleteButton" in request.form:
            #     Delete.comment(request.form["commentID"])
            #     return redirect(url_for("single_blog.single_blog", postID=postID)), 301
            if not session.get("userName"):
                flash(f"You are not logged in", "error")
                return redirect("/contact")
            verify_recaptcha(request.form.get("g-recaptcha-response"))
            verify_form(CommentForm(request.form))
            comment = request.form["comment"]
            parent_id = request.form.get("parent_id")
            to_eamil = post[5]
            if parent_id:
                cursor_comment.execute("""select user from comments where id = ? """, (parent_id,))
                parent_user = cursor_comment.fetchone()[0]
                to_eamil = parent_user
                cursor_comment.execute("insert into comments(post, comment, user, timeStamp, parent_id,parent_user) values(?, ?, ?, ?, ?,?)", (postID, comment, session["userName"], currentTime(), parent_id, parent_user))
            else:
                cursor_comment.execute("insert into comments(post, comment, user, timeStamp) values(?, ?, ?, ?)", (postID, comment, session["userName"], currentTime()))
            db_comment.commit()
            addPoints(5, session["userName"])  # 这里没有检查user是否存在
            flash("You earned 5 points by commenting.", "success")
            cursor_user.execute("""select email from users where userName = ? """, (to_eamil,))
            email = cursor_user.fetchone()[0]
            context = (ssl.create_default_context())
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(SMTP_MAIL, SMTP_PASSWORD)
            mail = EmailMessage()
            mail.set_content(f"Hi 👋,\n {session["userName"]} had give you a comment on {post[1]} ")
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
            mail["Subject"] = (f"👋🏻 {session["userName"]} commented on your blog {post[1]}")
            mail["From"] = SMTP_MAIL

            mail["To"] = email
            try:
                server.send_message(mail)
            except Exception as e:
                Log.danger(f"Comment to {parent_user} Incorrect email {e}")
            server.quit()
            # return redirect(url_for("single_blog.single_blog", postID=postID)), 301
        cursor_comment.execute("""select * from comments where post = ? order by timeStamp desc""", (postID,))
        comments = cursor_comment.fetchall()
        cursor_post.execute("""SELECT category, COUNT(*) FROM posts GROUP BY category ORDER BY category ASC """)
        categories = cursor_post.fetchall()
        cursor_post.execute(f"select id,title,banner,lastEditTimeStamp,category from posts order by lastEditTimeStamp desc limit 3")
        recent_posts = cursor_post.fetchall()
        for i in range(len(recent_posts)):
            tmp_post = list(recent_posts[i])
            base64_image = base64.b64encode(tmp_post[2]).decode('utf-8')
            tmp_post[2] = base64_image
            recent_posts[i] = tmp_post
        content = markdown_to_html(post[3])
        return render_template("single_blog.html", postid=post[0], title=post[1], tags=post[2].split(','), content=content, author=post[5], image=base64.b64encode(post[4]).decode('utf-8'), views=post[6], timeStamp=post[7], lastEditTimeStamp=post[8],
                               comments=comments, appName=APP_NAME, categories=categories, enumerate=enumerate, recent_posts=recent_posts, comments_nums=len(comments), siteKey=RECAPTCHA_SITE_KEY)
    else:
        flash(f"This {postID} blog cannot be found", "error")
        Log.danger(f"{request.remote_addr} tried to reach unknown post")
        return redirect("/")

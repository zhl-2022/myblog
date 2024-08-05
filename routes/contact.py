import smtplib
import ssl
from utils import *
from flask import render_template, flash, session, request, redirect, Blueprint, url_for, current_app
from passlib.hash import sha512_crypt as encryption
from constants import *
from email.message import EmailMessage
from routes import verify_recaptcha, verify_form
from models import User
contactBlueprint = Blueprint("contact", __name__)


@contactBlueprint.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        verify_recaptcha(request.form.get("g-recaptcha-response"))
        action = request.form.get('action')
        if action == 'login':
            verify_form(LoginForm(request.form))
            email = request.form["email"]
            password = request.form["password"]
            users_collection = current_app.mongo_db['users']
            user = users_collection.find_one({"email": email})
            if not user:
                flash("email not found.", "error")
            elif user["userName"] == session.get("userName"):
                flash("You are already logged in!", "success")
            else:
                if encryption.verify(password, user["password"]):
                    session["userName"] = user["userName"]
                    session["email"] = user["email"]
                    session["isVerified"] = user["isVerified"]
                    flash(f"Welcome, {user['userName']}!", "success")
                    return redirect("/")
                else:
                    flash("Wrong password.", "error")
        elif action == 'register':
            verify_form(SignUpForm(request.form))
            userName = request.form["userName"]
            email = request.form["email"]
            password = request.form["password"]
            passwordConfirm = request.form["passwordConfirm"]
            userName = userName.replace(" ", "")
            # 获取MongoDB集合
            users_collection = current_app.mongo_db['users']
            # 查询所有用户名和电子邮件
            users = users_collection.find({}, {"userName": 1, "email": 1})
            # 将查询结果转换为列表
            usernames = [user["userName"] for user in users]
            emails = [user["email"] for user in users]
            if userName in usernames and email in emails:
                flash("This username and email is unavailable.", "error")
            elif email in emails:
                flash("This email is unavailable.", "error")
            elif userName in usernames:
                flash("This username is unavailable.", "error")
            else:
                if passwordConfirm != password:
                    flash("Password must match.", "error")
                else:
                    if not userName.isascii():
                        flash("Username does not fit ascii charecters.", "error")
                    else:
                        password = encryption.hash(password)
                        # 获取MongoDB集合
                        # 插入新用户
                        new_user = User(userName, email, password)
                        users_collection.insert_one(new_user.todict())
                        session["userName"] = userName
                        session["email"] = email
                        session["isVerified"] = False
                        context = (ssl.create_default_context())
                        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                        server.ehlo()
                        server.starttls(context=context)
                        server.ehlo()
                        server.login(SMTP_MAIL, SMTP_PASSWORD)
                        mail = EmailMessage()
                        mail.set_content(f"Hi {userName}👋,\n Welcome to {APP_NAME}")
                        mail.add_alternative(
                            f"""\
                            <html>
                            <body>
                                <div
                                style="font-family: Arial, sans-serif;  max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius:0.5rem;"
                                >
                                <div style="text-align: center;">
                                    <h1 style="color: #F43F5E;">
                                    Hi {userName}, <br />
                                    Welcome to {APP_NAME}!
                                    </h1>
                                    <p style="font-size: 16px;">
                                    We are glad you joined us.
                                    </p>
                                </div>
                                </div>
                            </body>
                            </html>
                        """,
                            subtype="html")
                        mail["Subject"] = (f"Welcome to {APP_NAME}!👋🏻")
                        mail["From"] = SMTP_MAIL
                        mail["To"] = email
                        try:
                            server.send_message(mail)
                        except Exception as e:
                            flash(f"Incorrect email {e}", "error")
                            return redirect("/contact")
                        server.quit()
                        flash(f"Welcome, {userName}!", "success")
                        return redirect(url_for('verifyUser.verifyUser', codeSent='10'))
        elif action == 'forget':
            verify_form(ForgetForm(request.form))
            users_collection = current_app.mongo_db['users']
            user = users_collection.find_one({"email": request.form["email"]})
            if not user:
                flash("email not found.", "error")
                return redirect("/contact")
            return redirect(url_for('verifyUser.verifyUser', codeSent='20'))
    return render_template("contact.html", siteKey=RECAPTCHA_SITE_KEY)

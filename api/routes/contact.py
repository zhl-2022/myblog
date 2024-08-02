import smtplib
import ssl
from ..utils import *
from flask import render_template, flash, session, request, redirect, Blueprint, url_for
from passlib.hash import sha512_crypt as encryption
from ..constants import *
from email.message import EmailMessage
from . import verify_recaptcha, addPoints, verify_form
from ..factory import get_db2

contactBlueprint = Blueprint("contact", __name__)


@contactBlueprint.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        verify_recaptcha(request.form.get("g-recaptcha-response"))
        action = request.form.get('action')
        db_user = get_db2()
        cursor_user = db_user.cursor()
        if action == 'login':
            verify_form(LoginForm(request.form))
            email = request.form["email"]
            password = request.form["password"]
            cursor_user.execute("""select * from users where email = ? """, (email,))
            user = cursor_user.fetchone()
            if not user:
                flash("email not found.", "error")
            elif user[1] == session.get("userName"):
                flash("You are already logged in!", "success")
                return redirect("/contact")
            else:
                if encryption.verify(password, user[3]):
                    session["userName"] = user[1]
                    session["email"] = user[2]
                    session["role"] = user[5]
                    session["isVerified"] = user[8]
                    addPoints(1, user[1])
                    Log.success(f'USER: "{user[1]}" LOGGED IN')
                    flash(f"Welcome, {user[1]}!", "success")
                    return redirect("/contact")
                else:
                    flash("Wrong password.", "error")
        elif action == 'register':
            verify_form(SignUpForm(request.form))
            userName = request.form["userName"]
            email = request.form["email"]
            password = request.form["password"]
            passwordConfirm = request.form["passwordConfirm"]
            userName = userName.replace(" ", "")
            cursor_user.execute("select userName from users")
            users = str(cursor_user.fetchall())
            cursor_user.execute("select email from users")
            mails = str(cursor_user.fetchall())
            if userName in users and email in mails:
                flash("This username and email is unavailable.", "error")
            elif email in mails:
                flash("This email is unavailable.", "error")
            elif userName in users:
                flash("This username is unavailable.", "error")
            else:
                if passwordConfirm != password:
                    flash("Password must match.", "error")
                else:
                    if not userName.isascii():
                        flash("Username does not fit ascii charecters.", "error")
                    else:
                        password = encryption.hash(password)
                        cursor_user.execute(
                            f"""insert into users(userName,email,password,profilePicture,role,points,timeStamp,isVerified) values(?, ?, ?, ?, ?, ?, ?, ?)""",
                            (userName, email, password, f"{USER_PROFILE_PICTURE}{userName}{RADIUS_PROFILE_PICTURE}", "admin", 0, currentTime(), "False"))
                        db_user.commit()
                        session["userName"] = userName
                        session["email"] = email
                        session["role"] = "admin"
                        session["isVerified"] = "False"
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
                            Log.danger(f"Incorrect email {e}")
                            flash(f"Incorrect email {e}", "error")
                            return redirect("/contact")
                        server.quit()
                        addPoints(1, userName)
                        Log.success(f'User: "{userName}" logged in')
                        flash(f"Welcome, {userName}!", "success")
                        return redirect(url_for('verifyUser.verifyUser', codeSent='10'))
        elif action == 'forget':
            verify_form(ForgetForm(request.form))
            cursor_user.execute("""select * from users where email = ? """, (request.form["email"],))
            user = cursor_user.fetchone()
            if not user:
                flash("email not found.", "error")
                return redirect("/contact")
            return redirect(url_for('verifyUser.verifyUser', codeSent='20'))
    return render_template("contact.html", siteKey=RECAPTCHA_SITE_KEY)

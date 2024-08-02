# Import necessary modules and functions
from random import randint

from ..constants import *
from ..utils import *
import ssl
from flask import flash, redirect, render_template, request, session, Blueprint
from email.message import EmailMessage
import smtplib
from passlib.hash import sha512_crypt as encryption
from . import verify_recaptcha, verify_form
from ..factory import get_db2

verifyUserBlueprint = Blueprint("verifyUser", __name__)


@verifyUserBlueprint.route("/verifyUser/codesent=<codeSent>", methods=["GET", "POST"])
def verifyUser(codeSent):
    if request.method == "POST":
        verify_recaptcha(request.form.get("g-recaptcha-response"))
        if "email" in session:
            email = session["email"]
            db_user = get_db2()
            cursor_user = db_user.cursor()
            cursor_user.execute("""select isVerified,userName,password  from users where email = ? """, (email,))
            isVerified, userName, oldPassword = cursor_user.fetchone()
            if not userName:
                flash("User not found. Please change another email", "error")
                return redirect("/contact")
            if codeSent[0] == "1":  # 注册
                if isVerified == "True":
                    flash("Your account has been verified before", "success")
                    return redirect("/contact")
                else:
                    global verificationCode
                    if codeSent[1] == "1":  # 已经发送了验证码
                        verify_form(VerifyUserForm(request.form))
                        code = request.form["code"]
                        if code == verificationCode:
                            cursor_user.execute("""update users set isVerified = "True" where email= ? """, (email,))
                            db_user.commit()
                            session["isVerified"] = "True"
                            flash("Your account has been verified.", "success")
                            return redirect("/contact")
                        else:
                            flash("Wrong code.", "error")
                            return redirect("/verifyUser/codesent=10")
                    elif codeSent[1] == "0":  # 还没发送验证码
                        context = ssl.create_default_context()
                        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                        server.ehlo()
                        server.starttls(context=context)
                        server.ehlo()
                        server.login(SMTP_MAIL, SMTP_PASSWORD)
                        verificationCode = str(randint(1000, 9999))
                        message = EmailMessage()
                        message.set_content(f"Hi {userName}👋,\nHere is your account verification code🔢:\n{verificationCode}")
                        message.add_alternative(
                            f"""\
                                <html>
                                <body>
                                    <div
                                    style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius:0.5rem;"
                                    >
                                    <div style="text-align: center;">
                                        <h1 style="color: #F43F5E;">Thank you for creating an account!</h1>
                                        <p style="font-size: 16px;">
                                        Hello, {userName}.
                                        </p>
                                        <p style="font-size: 16px;">
                                        We are glad you joined us at {APP_NAME}. You can now enjoy our amazing
                                        features and services.
                                        </p>
                                        <p style="font-size: 16px;">
                                        To verify your email address, enter the following code in the app:
                                        </p>
                                        <span
                                        style="display: inline-block; background-color: #e0e0e0; color: #000000; padding: 10px 20px; font-size: 24px; font-weight: bold; border-radius: 0.5rem;"
                                        >{verificationCode}</span
                                        >
                                        <p style="font-size: 16px;">
                                        This code will expire when you refresh the page.
                                        </p>
                                        <p style="font-size: 16px;">
                                        Thank you for choosing {APP_NAME}.
                                        </p>
                                    </div>
                                    </div>
                                </body>
                                </html>
                        """,
                            subtype="html",
                        )
                        message["Subject"] = "Verification Code🔢"
                        message["From"] = SMTP_MAIL
                        message["To"] = email
                        try:
                            server.send_message(message)
                        except Exception as e:
                            Log.danger(f"Incorrect email {e}")
                            flash(f"Incorrect email {e}", "error")
                            return redirect("/contact")
                        server.quit()
                        flash("verificationCode sent.", "success")
                        return redirect("/verifyUser/codesent=11")
            elif codeSent[0] == "2":  # 修改密码
                global passwordResetCode
                if codeSent[1] == "1":  # 已发送验证
                    verify_form(ForgetForm(request.form))
                    code = request.form["code"]
                    password = request.form["password"]
                    passwordConfirm = request.form["passwordConfirm"]
                    if password != passwordConfirm:
                        flash("Password must match.", "error")
                        return redirect("/verifyUser/codesent=20")
                    if code != passwordResetCode:
                        flash("Wrong code.", "error")
                        return redirect("/verifyUser/codesent=20")
                    if encryption.verify(password, oldPassword):
                        flash("New password cannot be the same as the old password.", "error")
                        return redirect("/verifyUser/codesent=20")
                    else:
                        password = encryption.hash(password)
                        cursor_user.execute("""update users set password = ? where email = ? """, (password, email))
                        db_user.commit()
                        flash("You need to login with the new password.", "success")
                        return redirect("/contact")
                elif codeSent[1] == "0":
                    context = ssl.create_default_context()
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                    server.ehlo()
                    server.starttls(context=context)
                    server.ehlo()
                    server.login(SMTP_MAIL, SMTP_PASSWORD)
                    passwordResetCode = str(randint(1000, 9999))
                    message = EmailMessage()
                    message.set_content(
                        f"Hi {userName}👋,\nForgot your password😶‍🌫️? No problem👌.\nHere is your password reset code🔢:\n{passwordResetCode}"
                    )
                    message.add_alternative(
                        f"""\
                        <html>
                        <body style="font-family: Arial, sans-serif;">
                        <div style="max-width: 600px;margin: 0 auto;background-color: #ffffff;padding: 20px; border-radius:0.5rem;">
                            <div style="text-align: center;">
                            <h1 style="color: #F43F5E;">Password Reset</h1>
                            <p>Hello, {userName}.</p>
                            <p>We received a request to reset your password for your account. If you did not request this, please ignore this email.</p>
                            <p>To reset your password, enter the following code in the app:</p>
                            <span style="display: inline-block; background-color: #e0e0e0; color: #000000;padding: 10px 20px;font-size: 24px;font-weight: bold; border-radius: 0.5rem;">{passwordResetCode}</span>
                            <p style="font-family: Arial, sans-serif; font-size: 16px;">This code will expire when you refresh the page.</p>
                            <p>Thank you for using {APP_NAME}.</p>
                            </div>
                        </div>
                        </body>
                        </html>
                    """,
                        subtype="html")
                    message["Subject"] = "Forget Password?🔒"
                    message["From"] = SMTP_MAIL
                    message["To"] = email
                    try:
                        server.send_message(message)
                    except Exception as e:
                        Log.danger(f"Incorrect email {e}")
                        flash(f"Incorrect email {e}", "error")
                        return redirect("/contact")
                    server.quit()
                    flash("passwordResetCode sent.", "success")
                    return redirect("/verifyUser/codesent=21")
        else:
            flash("Your session has no email information", "error")
            return redirect("/contact")
    else:
        return render_template("verifyUser.html", codeSent=codeSent, siteKey=RECAPTCHA_SITE_KEY)

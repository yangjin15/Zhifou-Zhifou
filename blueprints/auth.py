import os
from flask import Blueprint, render_template, jsonify, redirect, url_for, session , g , flash
from werkzeug.utils import secure_filename
from exts import mail, db
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptchaModel, UserModel
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")

from flask import current_app

@bp.route("/profile", methods=['GET', 'POST'])
def profile():
    if not g.user:
        flash("请先登录再访问该页面。")
        return redirect(url_for("auth.login"))

    if request.method == 'POST':
        user = g.user
        user.bio = request.form.get('bio')
        avatar = request.files.get('avatar')
        if avatar:
            filename = secure_filename(avatar.filename)
            avatar_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            avatar.save(avatar_path)
            user.avatar = filename
        db.session.commit()
        flash("个人资料更新成功！")
        return redirect(url_for('auth.profile'))
    return render_template("profile.html")



@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱在数据库中不存在！")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password, password):
                # if password == user.password :
                session['user_id'] = user.id
                return redirect("/")
            else:
                print("密码错误！")
                # print(password)
                # print(user.password)
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            # return redirect(url_for("auth.register"))
            return "no"


@bp.route("/captcha/email")
def get_email_captcha():
    email = request.args.get("email")
    source = string.digits * 4
    captcha = random.sample(source, 4)
    captcha = "".join(captcha)
    message = Message(subject="邮件", recipients=[email], body=f"您的验证码是：{captcha}")
    mail.send(message)

    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()

    return jsonify({"code": 200, "message": "", "data": None})


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮件", recipients=["2265712846@qq.com"], body="这个是测试")
    mail.send(message)
    return "发件成功"

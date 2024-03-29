# package level dependencies :
from npl import app, db
from npl.models import Team, Student
from npl.views_utils import encrypt_password, send_ack_mail


# flask related dependencies :
from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/student/<student_email>/dashboard")
def student_dashboard(student_email):
    student = Student.query.filter_by(email=student_email).first()
    return render_template("student_dashboard.html", student=student)


@app.route("/register/student", methods=['GET', 'POST'])
def student_register():
    if request.method == "GET":
        return render_template("student_register.html")

    elif request.method == "POST":
        student_name = request.form.get("student_name")
        student_email = request.form.get("student_email")
        institute_name = request.form.get("institute_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if Student.query.filter_by(email=student_email).first():
            flash(message="This email is Taken", category="warning")
            return redirect(url_for('student_register'))

        if password == confirm_password:
            Student.add_student(
                student_name=student_name,
                student_email=student_email,
                institute_name=institute_name,
                password=password,
            )

            send_ack_mail(email=student_email, ack_info="You are successfully registered. You can login with your registered username and password.")
            flash(message="You are registered successfully, check your email for confirmation!", category="success")
            return redirect(url_for('home'))
        else:
            flash(message="Passwords do not match.", category="warning")
            return redirect(url_for('student_register'))


@app.route("/login/student", methods=['GET', 'POST'])
def student_login():
    if request.method == "GET":
        return render_template("student_login.html")
    elif request.method == "POST":
        student_email = request.form.get("student_email")
        password = request.form.get("password")

        student = Student.query.filter_by(email=student_email).first()

        if student and check_password_hash(student.password, password):
            flash(message='Login Success!', category='success')
            return redirect(url_for('student_dashboard', student_email=student_email))

        flash('Please check your login details and try again.')
        return redirect(url_for('student_login'))

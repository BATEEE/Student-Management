from flask import request, redirect, render_template
from dao import add_subject, find_student, remove_student
from init import app, login
from admin import *
import dao
from flask_login import login_user, logout_user, current_user


@app.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect('/login')
    else:
        return render_template("index.html")

@app.route("/login", methods=['get', 'post'])
def login_user_process():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_login(username=username, password=password)
        if user:
            login_user(user)
            direct = str(user.user_role).split('.')[1].lower()
            return redirect('/' + direct)
        else:
            err_msg = "Tài khoản hoặc mật khẩu của bạn không chính xác"
    return render_template("login.html", err_msg=err_msg)

# Quản lý môn học: thêm môn học
@app.route("/subject", methods=['get', 'post'])
def subject():
    if request.method.__eq__('POST'):
        id = request.form.get('mon_hoc_id')
        ten_mon_hoc = request.form.get('ten_mon_hoc')

        add_subject(id, ten_mon_hoc)

    return render_template("subject.html")

@app.route('/nv')
def employee():
    return render_template('ems/employee.html')

@app.route('/nv/add', methods=['get', 'post'])
def add_student():
    theme_name = "Thêm học sinh"

    if request.method.__eq__('POST'):
        id = request.form.get('id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        date = request.form.get('birthday')
        sex = request.form.get('sex')

    return render_template("ems/add_student.html", theme_name=theme_name)

@app.route('/nv/search')
def search_student():
    theme_name = "Tìm kiếm học sinh"
    return render_template("ems/search_student.html", theme_name=theme_name)

@app.route('/nv/update', methods=['get', 'post'])
def update_student():
    student = None

    if request.method.__eq__('GET'):
        id = request.args.get('id')
        student = find_student(id)
    elif request.method.__eq__('POST'):
        remove_student(id)
    theme_name = "Cập nhật thông tin học sinh"
    return render_template("ems/update_student.html", theme_name=theme_name, student=student)

@app.route("/qt")
def admin():
    return render_template("admin/index.html")

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)
    

if __name__ == '__main__':
    app.run(debug=True)

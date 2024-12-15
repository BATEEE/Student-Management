from flask import request, redirect, render_template
from dao import add_subject
from init import app, login
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

# Nhân viên: Thêm học sinh
@app.route("/qt", methods=['get', 'post'])
def add_student():
    if request.method.__eq__('POST'):
        id = request.form.get('id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        date = request.form.get('birthday')
        sex = request.form.get('sex')

    return render_template("ems/add_student.html")

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)
    

if __name__ == '__main__':
    app.run(debug=True)
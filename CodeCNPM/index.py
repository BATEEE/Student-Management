from flask import request, redirect, render_template, session, abort
from functools import wraps
import dao
from init import app, login
from flask_login import login_user, current_user
from models import HocSinh


@app.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect('/login')
    else:
        return render_template("index.html")

def role_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] not in allowed_roles:
                abort(403)  # Trả về lỗi 403 Forbidden
            return func(*args, **kwargs)
        return wrapper
    return decorator

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
            session['role'] = direct
            if direct.__eq__('qt'):
                direct = 'admin'
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

        dao.add_subject(id, ten_mon_hoc)

    return render_template("subject.html")

@app.route('/nv')
@role_required(['nv'])
def employee():
    return render_template('ems/employee.html')

@app.route('/nv/add', methods=['get', 'post'])
@role_required(['nv'])
def add_student_process():
    theme_name = "Thêm học sinh"
    student_id = None
    if request.method.__eq__('POST'):
        count = str(HocSinh.query.count() + 1)
        student_id = 'HS' + '0' * (4 - len(count)) + count
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        date = request.form.get('birthday')
        sex = request.form.get('sex')
        address = request.form.get('address')
        contact = request.form.get('contact')
        email = request.form.get('email')

        dao.add_student(id=student_id, ho=first_name, ten=last_name, gioi_tinh=sex, dia_chi=address, email=email, ngay_sinh=date, so_dien_thoai=contact)

    count = str(HocSinh.query.count() + 1)
    return render_template("ems/add_student.html", theme_name=theme_name,
                           count=count, len_of_count=len(count))

@app.route('/nv/search')
@role_required(['nv'])
def search_student():
    theme_name = "Tìm kiếm học sinh"
    id = request.args.get('id')
    student = dao.find_student_class(id)
    return render_template("ems/search_student.html", theme_name=theme_name, student=student)

@app.route('/nv/update', methods=['get', 'post'])
@role_required(['nv'])
def update_student():
    student = None
    id = request.args.get('id')

    if request.method.__eq__('GET'):
        student = dao.find_student(id)
    elif request.method.__eq__('POST'):
        ho = request.form.get('first_name')
        ten = request.form.get('last_name')
        gioi_tinh = request.form.get('sex')
        dia_chi = request.form.get('address')
        email = request.form.get('email')
        ngay_sinh = request.form.get('date')
        so_dien_thoai = request.form.get('contact')
        dao.update_studentinfo(id=id, ho=ho, ten=ten, gioi_tinh=int(gioi_tinh), dia_chi=dia_chi, email=email, ngay_sinh=ngay_sinh, so_dien_thoai=so_dien_thoai)

    theme_name = "Cập nhật thông tin học sinh"
    return render_template("ems/update_student.html", theme_name=theme_name, student=student)

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)
    

if __name__ == '__main__':
    with app.app_context():
        from admin import admin
        app.run(debug=True)

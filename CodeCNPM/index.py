import datetime
from flask import request, redirect, render_template, session, abort, jsonify
from functools import wraps
import dao
from flask_login import login_user, current_user
from models import HocSinh, ThongTinNamHoc, Lop, HocSinhThuocLop, QuyDinh
from models import HocSinh, ThongTinNamHoc, Lop
from init import app, login
from flask_login import login_user, current_user, login_required, logout_user
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
@login_required
def employee():
    return render_template('ems/employee.html')


@app.route('/nv/add', methods=['get', 'post'])
@role_required(['nv'])
@login_required
def add_student_process():
    theme_name = "Thêm học sinh"
    student_id = None
    msg = ""
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
        if datetime.datetime.now().year - int(date[:4]) >= 15 and datetime.datetime.now().year - int(date[:4]) <= 20:
            dao.add_student(id=student_id, ho=first_name, ten=last_name, gioi_tinh=sex, dia_chi=address, email=email,
                        ngay_sinh=date, so_dien_thoai=contact)
            msg = "Thêm thành công"
        else:
            msg = "Số tuổi yêu cầu từ 15 đến 20"

    count = str(HocSinh.query.count() + 1)
    return render_template("ems/add_student.html", theme_name=theme_name,
                           count=count, len_of_count=len(count), msg=msg)


@app.route('/nv/search')
@role_required(['nv'])
@login_required
def search_student():
    theme_name = "Tìm kiếm học sinh"
    id = request.args.get('id')
    student = dao.find_student(id)
    return render_template("ems/search_student.html", theme_name=theme_name, student=student)


@app.route('/nv/update', methods=['get', 'post'])
@role_required(['nv'])
@login_required
def update_student():
    student = None
    id = request.args.get('id')

    if request.method.__eq__('GET') and 'id' in request.args:
        student = dao.find_student(id)
    elif request.method.__eq__('POST'):
        ho = request.form.get('first_name')
        ten = request.form.get('last_name')
        gioi_tinh = request.form.get('sex')
        dia_chi = request.form.get('address')
        email = request.form.get('email')
        ngay_sinh = request.form.get('date')
        so_dien_thoai = request.form.get('contact')
        dao.update_studentinfo(id=id, ho=ho, ten=ten, gioi_tinh=int(gioi_tinh), dia_chi=dia_chi, email=email,
                               ngay_sinh=ngay_sinh, so_dien_thoai=so_dien_thoai)

    theme_name = "Cập nhật thông tin học sinh"
    return render_template("ems/update_student.html", theme_name=theme_name, student=student)


@app.route('/nv/make_profile', methods=['get', 'post'])
@role_required(['nv'])
@login_required
def make_profile_student():
    theme_name = "Tạo hồ sơ học sinh"
    count = str(HocSinh.query.count() + 1)
    student_id = None
    if request.method.__eq__('POST'):
        student_id = 'HS' + '0' * (4 - len(count)) + count
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        date = request.form.get('birthday')
        sex = request.form.get('sex')
        address = request.form.get('address')
        contact = request.form.get('contact')
        email = request.form.get('email')

        dao.add_student(id=student_id, ho=first_name, ten=last_name, gioi_tinh=sex, dia_chi=address, email=email,
                        ngay_sinh=date, so_dien_thoai=contact)

    return render_template("ems/make_profile_student.html", theme_name=theme_name,
                           count=count, len_of_count=len(count))


@app.route('/nv/create_class', methods=['get', 'post'])
@role_required(['nv'])
@login_required
def create_class():
    theme_name = "Lập danh sách lớp"
    list_class = dao.get_all_class()
    number_of_class = session.get('number_of_class')
    if not number_of_class:
        session['number_of_class'] = 0
    class_id = session.get('class_id')
    if not class_id:
        session['class_id'] = 0
    if request.method.__eq__('GET') and 'number_of_class' in request.args:
        session['class_id'] = request.args.get('class_id')
        session['number_of_class'] = request.args.get('number_of_class')
        if int(session['number_of_class']) > QuyDinh.SI_SO:
            session['number_of_class'] = QuyDinh.SI_SO
        elif int(session['number_of_class']) <= 0:
            session['number_of_class'] = 1
        list_student = dao.create_class(class_id=session['class_id'], number_of_class=session['number_of_class'])
        session['number_of_class'] = len(list_student)
        list_student_js = []
        for i in list_student:
            student = {
                "id": i.id,
                "ho_ten": i.ho + " " + i.ten,
                "gioi_tinh": i.gioi_tinh,
                "nam_sinh": i.ngay_sinh.year,
                "dia_chi": i.dia_chi
            }
            list_student_js.append(student)
        session['list_student'] = list_student_js
        return render_template('ems/create_class.html', theme_name=theme_name, list_class=list_class, selected_id=int(session['class_id']),
                               list_student=list_student_js)
    elif request.method.__eq__('POST'):
        list_student = session['list_student']
        dao.add_student_into_class(list_student=list_student, class_id=session['class_id'])
        session['list_student'] = []
        list_student = session['list_student']
        return render_template('ems/create_class.html', theme_name=theme_name, list_class=list_class,
                               selected_id=int(session['class_id']), list_student=list_student
                               , number_of_class=session['number_of_class'])
    return render_template('ems/create_class.html', theme_name=theme_name, list_class=list_class, selected_id=1, list_student=[]
                         , number_of_class=0)


@app.route("/api/create_class/<hoc_sinh_id>", methods=['delete'])
def delete_student(hoc_sinh_id):
    list_student :list= session.get('list_student')
    for student in list_student:
        if student['id'].__eq__(hoc_sinh_id):
            list_student.remove(student)
            session['list_student'] = list_student
            return jsonify({"success": True, "message": "Học sinh đã được xóa"})
    return jsonify({"success": False, "message": "Học sinh không tồn tại"})

#Dieu chinh lop
@app.route('/nv/adjust_class')
@role_required(['nv'])
@login_required
def adjust_class():
    theme_name = "Điều chỉnh danh sách lớp"
    danhsachlop=dao.get_hocsinh_lop()
    return render_template('ems/adjust_class.html', theme_name=theme_name,danhsachlop=danhsachlop)

@app.route('/nv/adjust_class/get_listStudent',methods=['GET'])
def get_hocSinhTheoLop():
    idLop=request.args.get('id_lop')
    result=dao.get_listHocSinh_lop(idLop)
    listStudent = [{
        'id': student.id,
        'ho': student.ho,
        'ten': student.ten,
        'gioi_tinh': student.gioi_tinh,
        'ngay_sinh': student.ngay_sinh.strftime('%d-%m-%Y'),
        'dia_chi': student.dia_chi
    } for student in result]
    return jsonify(listStudent)


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/admin/get_hocki', methods=['GET'])
def get_hocki():
    nam_hoc = request.args.get('nam_hoc')
    hocki_list = db.session.query(
        ThongTinNamHoc.hoc_ki
    ).filter(ThongTinNamHoc.nam_hoc == nam_hoc).distinct().all()
    result = [row[0] for row in hocki_list]
    return jsonify(result)


@app.route("/logout")
@login_required
def log_out():
    logout_user()
    return redirect('login')


#
@app.route('/admin/get_thongke', methods=['GET'])
def get_thongke():
    nam_hoc = request.args.get('nam_hoc')
    hoc_ki = request.args.get('hoc_ki')
    monhoc = request.args.get('mon_hoc')
    thongke = dao.thongke_DatMon(mon=monhoc, nam=nam_hoc, hocki=hoc_ki)
    result = [
        {
            'ten_lop': row[0],
            'hoc_sinh': row[1],
            'diem_trung_binh': row[2]
        } for row in thongke
    ]
    return jsonify(result)


if __name__ == '__main__':
    with app.app_context():
        from admin import admin

        app.run(debug=True, port=2004)

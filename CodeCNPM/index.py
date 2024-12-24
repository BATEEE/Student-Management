import datetime
from flask import request, redirect, render_template, session, abort, jsonify
from functools import wraps
import dao
from flask_login import login_user, current_user
from models import HocSinh, ThongTinNamHoc, Lop, HocSinhThuocLop, QuyDinh, NhanVien, GiaoVien, NamHocHienTai
from models import HocSinh, ThongTinNamHoc, Lop
from init import app, login, db
from flask_login import login_user, current_user, login_required, logout_user
from models import HocSinh


# @app.route("/")
# def index():
#     if not current_user.is_authenticated:
#         return redirect('/login')
#     else:
#         return render_template("index.html")


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
            elif direct.__eq__('gv'):
                direct = ''
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
    nv = NhanVien.query.filter(NhanVien.tai_khoan_id.__eq__(current_user.id)).first()
    return render_template('ems/employee.html', nv=nv)


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
        if datetime.datetime.now().year - int(date[:4]) >= QuyDinh.AGE_MIN and datetime.datetime.now().year - int(date[:4]) <= QuyDinh.AGE_MAX:
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
                               list_student=list_student_js, nam_hoc=NamHocHienTai.NAM_HOC, hoc_ky=str(NamHocHienTai.HOC_KY))
    elif request.method.__eq__('POST'):
        list_student = session['list_student']
        dao.add_student_into_class(list_student=list_student, class_id=session['class_id'])
        session['list_student'] = []
        list_student = session['list_student']
        return render_template('ems/create_class.html', theme_name=theme_name, list_class=list_class,
                               selected_id=int(session['class_id']), list_student=list_student
                               , number_of_class=session['number_of_class'], nam_hoc=NamHocHienTai.NAM_HOC, hoc_ky=str(NamHocHienTai.HOC_KY))
    return render_template('ems/create_class.html', theme_name=theme_name, list_class=list_class, selected_id=1, list_student=[]
                         , number_of_class=0, nam_hoc=NamHocHienTai.NAM_HOC, hoc_ky=str(NamHocHienTai.HOC_KY))


@app.route("/api/create_class/<hoc_sinh_id>", methods=['delete'])
def delete_student(hoc_sinh_id):
    list_student :list= session.get('list_student')
    for student in list_student:
        if student['id'].__eq__(hoc_sinh_id):
            list_student.remove(student)
            session['list_student'] = list_student
            return jsonify({"success": True, "message": "Học sinh đã được xóa"})
    return jsonify({"success": False, "message": "Học sinh không tồn tại"})

#Xoa hoc sinh khoi lop
@app.route("/api/adjust_class/<hoc_sinh_id>&<class_id>", methods=['delete'])
def delete_student_class(hoc_sinh_id,class_id):
    if dao.delete_hocsinh(idHocSinh=hoc_sinh_id,idLop=class_id):
         db.session.commit()
         return jsonify({"success":True, "message": "Xóa học sinh thành công!"})
    return jsonify({"success": False, "message": "Xóa học sinh không thành công!"})

#Dieu chinh lop
@app.route('/nv/adjust_class')
@role_required(['nv'])
@login_required
def adjust_class():
    theme_name = "Điều chỉnh danh sách lớp"
    danhsachlop=dao.get_hocsinh_lop()
    return render_template('ems/adjust_class.html', theme_name=theme_name,danhsachlop=danhsachlop,quydinh=QuyDinh)

#Lay danh sach hoc sinh theo lop
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

#Them hoc sinh moi khi dieu chinh lop
@app.route('/nv/adjust_class',methods=['POST'])
@role_required(['nv'])
@login_required
def dieuChinhLop_themHocSinh():
    data=request.get_json()
    student_obj=data['students']
    class_id=student_obj[0]['id_class']
    # list_student_class=dao.get_listHocSinh_lop(class_id)
    dao.add_student_into_class(list_student=student_obj,class_id=class_id)
    return jsonify({"success": True, "message": "Học sinh đã được thêm vào lớp"})

@app.route('/nv/adjust_class/get_hocSinh',methods=['GET'])
@role_required(['nv'])
@login_required
def dieuChinhLop_getHocSinh():
    student_id=request.args.get('student_id')
    class_id=request.args.get('class_id')
    siSo=request.args.get('si_so')
    list_student_class = dao.get_listHocSinh_lop(class_id)
    kiemtrahocsinhcolop=dao.kiemtra_hocsinh_lop(student_id)

    if int(siSo)>=QuyDinh.SI_SO:
        mess = "Quá số lượng học sinh quy định."
        return jsonify({'message': mess})
    if kiemtrahocsinhcolop:
        return jsonify([])
    for item in list_student_class:
        if item[0].__eq__(student_id):
            return jsonify([])
    result=dao.get_hocsinh(student_id)
    if result :
        sex={True:"Nữ", False: "Nam"} [result[3]]
        student={
            "id":result[0],
            "ho_ten":result[1]+" "+result[2],
            "gioi_tinh":sex,
            "ngay_sinh": result[4].strftime("%d-%m-%Y"),
            "dia_chi": result[5]

        }
        return jsonify(student)
    return jsonify([])


#Trang Giao Vien
@app.route('/gv')
@role_required(['gv'])
@login_required
def teacher():
    gv = GiaoVien.query.filter(GiaoVien.tai_khoan_id.__eq__(current_user.id)).first()
    return render_template('teacher/teacher.html', gv=gv)


@app.route('/gv/nhap_diem')
@role_required(['gv'])
@login_required
def nhap_diem():
    theme_name = "Nhập điểm"
    list_class = dao.get_list_class_of_teacher()
    return render_template('teacher/nhapdiem.html', theme_name=theme_name, list_class=list_class
                           , hoc_ki=NamHocHienTai.HOC_KY, nam_hoc=NamHocHienTai.NAM_HOC)

@app.route("/api/gv/get-subject/<class_id>", methods=['post'])
def get_class(class_id):
    data = request.get_json()
    list_subject = dao.get_subject_of_teacher_in_class(data['class_id'])
    subject_json = []
    for subject in list_subject:
        json = {
            "id": subject.giao_vien_day_mon.mon_hoc.id,
            "ten_mon_hoc": subject.giao_vien_day_mon.mon_hoc.ten_mon_hoc
        }
        subject_json.append(json)
    return jsonify(subject_json)

@app.route('/api/gv/nhap_diem', methods=['post'])
def get_list_student():
    data = request.get_json()
    list_student = dao.get_listHocSinh_lop(data['class_id'])
    list_student_json = []
    for student in list_student:
        list_student_json.append({
            "student_id": student.id,
            "name": student.ho + " " + student.ten
        })
    return jsonify(list_student_json)

@app.route('/api/gv/get-score', methods=['post'])
def get_score():
    data = request.get_json()
    phut_15 = int(data['number_15'])
    phut_45 = int(data['number_45'])
    trang_thai = {}
    for score in data['student_score']:
        trang_thai = dao.save_score(student_id=score[0], subject_id=data['subject_id'],
                       score_15=score[1][:phut_15]
                       , score_45=score[1][phut_15:phut_15 + phut_45], score_cuoi_ky=[score[1][-1]])
        if trang_thai['success'].__eq__("fail"):
            break
    return jsonify(trang_thai)

@app.route("/api/gv/nhap_diem/xem_diem", methods=['get'])
def xem_diem():
    class_id = request.args.get("class_id")
    subject_id = request.args.get("subject_id")
    list_student = dao.get_listHocSinh_lop(class_id)
    score_all_student = []
    for student in list_student:
        score_of_student = dao.get_score(subject_id, student)
        score_js = {
            "name": student.ho + " " + student.ten,
            "score": {
                "test_15": score_of_student[0],
                "test_45": score_of_student[1],
                "test_ck": score_of_student[2]
            }
        }
        score_all_student.append(score_js)
    return jsonify(score_all_student)

@app.route('/gv/xuat_diem')
@role_required(['gv'])
@login_required
def xuat_diem():
    theme_name = "Xuất điểm"
    list_class = dao.get_list_class_of_teacher()
    list_namhoc=dao.get_namhoc_giaovienday()
    return render_template('teacher/xuatdiem.html', theme_name=theme_name,list_class=list_class,list_namhoc=list_namhoc)


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


#lay lop theo nam hoc
@app.route('/gv/xuat_diem/getclass', methods=['GET'])
def get_lopTheoNamHoc():
    nam_hoc = request.args.get('namHoc')
    result=dao.get_lop_namhoc(nam_hoc)
    name_class={
        "id": result.lop.id,
        "ten_lop":result.lop.ten_lop
    }
    return jsonify(name_class)
#Lay hoc sinh bao cao diem
@app.route('/api/gv/xuat_diem', methods=['POST'])
def get_hocSinhBaoCaoDiem():
    data= request.get_json()
    result=dao.get_diemTB_hocKi(tenlop=data['ten_lop'],namhoc=data['nam_hoc'])
    if not result:
        return jsonify([])
    list_students={}
    for item in result:
        if item[0] not in list_students:
            list_students[item[0]] = {
                'ten_hoc_sinh': item[1],
                'ten_lop': item[2],
                'tb_hk1': None,
                'tb_hk2': None
            }
        if item[3] == 1:
            list_students[item[0]]['tb_hk1'] = item[4]
        elif item[3] == 2:
            list_students[item[0]]['tb_hk2'] = item[4]
    # list_students = [
    #     {
    #         'ten_hoc_sinh': student_data['ten_hoc_sinh'],
    #         'ten_lop': student_data['ten_lop'],
    #         'tb_hk1': student_data['tb_hk1'],
    #         'tb_hk2': student_data['tb_hk2']
    #     }
    #     for student_data in result.values()
    # ]
    return jsonify(list_students)

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
        app.run(debug=True)

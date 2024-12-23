from fileinput import hook_compressed

from flask import session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import query_expression
from flask_login import current_user
from models import TaiKhoan, UserRole, GiaoVien, QuanTri, MonHoc, HocSinh, HocSinhThuocLop, Lop, LoaiDiem, Diem, \
HocSinhHocMon, ThongTinNamHoc, NamHocHienTai, NhanVien, Day, GiaoVienDayMon

from init import db
from sqlalchemy import func, asc
from datetime import datetime
import hashlib

def auth_login(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return TaiKhoan.query.filter(TaiKhoan.tai_khoan.__eq__(username.strip()),
                                 TaiKhoan.mat_khau.__eq__(password)).first()

def add_user(username, password, role):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    n = TaiKhoan.query.count() # so luong user trong Tai Khoan


# thêm môn học
def add_subject(id, ten_mon_hoc):
    mon_hoc = MonHoc(id=id, ten_mon_hoc=ten_mon_hoc)
    db.session.add(mon_hoc)
    db.session.commit()

# thêm học sinh
def add_student(id, ho, ten, gioi_tinh, dia_chi, email, ngay_sinh, so_dien_thoai):
    hoc_sinh = HocSinh(id=id, ho=ho, ten=ten, gioi_tinh=int(gioi_tinh), dia_chi=dia_chi, email=email,
                       ngay_sinh=ngay_sinh, so_dien_thoai=so_dien_thoai)
    db.session.add(hoc_sinh)
    db.session.commit()

def get_user_by_id(id):
    return TaiKhoan.query.get(id)

def find_student_class(id):
    student_class = HocSinhThuocLop.query \
        .filter(HocSinhThuocLop.hoc_sinh_id == id) \
        .join(HocSinhThuocLop.thong_tin_nam_hoc) \
        .order_by(ThongTinNamHoc.nam_hoc.desc(), ThongTinNamHoc.hoc_ki.desc()) \
        .first()
    return student_class

def find_student(id):
    if not id:
        return []
    student = HocSinh.query.filter(HocSinh.id.__eq__(id)).first()
    student_class = find_student_class(student.id)
    if student_class:
        return {
            "id": student_class.hoc_sinh.id,
            "ho": student_class.hoc_sinh.ho,
            "ten": student_class.hoc_sinh.ten,
            "dia_chi": student_class.hoc_sinh.dia_chi,
            "ngay_sinh": student_class.hoc_sinh.ngay_sinh,
            "gioi_tinh": student_class.hoc_sinh.gioi_tinh,
            "ten_lop": student_class.lop.ten_lop,
            "so_dien_thoai": student_class.hoc_sinh.so_dien_thoai,
            "email": student_class.hoc_sinh.email,
        }
    return {
            "id": student.id,
            "ho": student.ho,
            "ten": student.ten,
            "dia_chi": student.dia_chi,
            "ngay_sinh": student.ngay_sinh,
            "gioi_tinh": student.gioi_tinh,
            "ten_lop": "Không có lớp",
            "so_dien_thoai": student.so_dien_thoai,
            "email": student.email,
        }

# Lay danh sach lop hoc
def get_all_class(khoi_lop=[10, 11, 12]):
    return Lop.query.filter(Lop.khoi_lop.in_(khoi_lop)).all()

# Them hoc sinh vao lop
def add_student_into_class(list_student, class_id):
    thong_tin_nam_hoc = ThongTinNamHoc.query.filter(ThongTinNamHoc. nam_hoc.__eq__(NamHocHienTai.NAM_HOC), ThongTinNamHoc.hoc_ki.__eq__(NamHocHienTai.HOC_KY)).first()
    for k in list_student:
        hoc_sinh_thuoc_lop = HocSinhThuocLop(hoc_sinh_id=k['id'], lop_id=class_id, thong_tin_nam_hoc_id=thong_tin_nam_hoc.id)
        db.session.add(hoc_sinh_thuoc_lop)
        db.session.commit()

# Tao danh sach lop
def create_class(number_of_class, class_id):
    # Lấy danh sách lớp
    lop = Lop.query.filter(Lop.id.__eq__(class_id)).first()
    # Lấy thông tin năm học của kỳ trước ví dụ học kỳ 2 thì xuống học kỳ 1 còn năm thì giảm nếu học kỳ là 1 còn nếu học kỳ là 2 thì sẽ giữ nguyên
    nam_hoc, hoc_ky, khoi_lop = (int(NamHocHienTai.NAM_HOC), 1, lop.khoi_lop) if NamHocHienTai.HOC_KY.__eq__(2) else (int(NamHocHienTai.NAM_HOC) - 1, 2, lop.khoi_lop - 1)
    # Lấy danh sách học sinh đã học ở kỳ trước tương đương khối lớp đã học ở kỳ trước
    student_last_year = db.session.query(HocSinh).join(HocSinhThuocLop, HocSinhThuocLop.hoc_sinh_id.__eq__(HocSinh.id)) \
                        .join(ThongTinNamHoc, HocSinhThuocLop.thong_tin_nam_hoc_id.__eq__(ThongTinNamHoc.id)) \
                        .join(Lop, HocSinhThuocLop.lop_id.__eq__(Lop.id)) \
                        .filter(ThongTinNamHoc.nam_hoc.__eq__(nam_hoc), ThongTinNamHoc.hoc_ki.__eq__(hoc_ky), Lop.khoi_lop.__eq__(khoi_lop)).subquery()
    # student_current_year = HocSinhThuocLop.query.filter(HocSinhThuocLop.thong_tin_nam_hoc.nam_hoc.__eq__(NamHocHienTai.NAM_HOC)).all()
    student_of_class = (HocSinhThuocLop.query.join(HocSinhThuocLop.thong_tin_nam_hoc)
                        .filter(ThongTinNamHoc.nam_hoc.__eq__(NamHocHienTai.NAM_HOC), ThongTinNamHoc.hoc_ki.__eq__(NamHocHienTai.HOC_KY)).all()) # Lấy danh sách học sinh đã có lớp
    new_students = [x.hoc_sinh_id for x in student_of_class]  # Lọc học sinh đã có lớp và học sinh chưa có
    # random từ danh sách học sinh bỏ đi danh sách học sinh của new student vì chỉ cần lấy danh sách học sinh chưa có lớp
    random_student = db.session.query(student_last_year).filter(student_last_year.c.id.notin_(new_students)).order_by(func.random()).order_by(student_last_year.c.ten.asc()).limit(number_of_class).all()
    return random_student

# sửa thông tin học sinh
def update_studentinfo(id, ho, ten, gioi_tinh, dia_chi, email, ngay_sinh, so_dien_thoai):
    student = HocSinh.query.filter(HocSinh.id.__eq__(id)).first()
    if student:
        student.ho = ho
        student.ten = ten
        student.gioi_tinh = gioi_tinh
        student.dia_chi = dia_chi
        student.email = email
        student.ngay_sinh = ngay_sinh
        student.so_dien_thoai = so_dien_thoai
        db.session.commit()

#Lay du lieu mon hoc
def get_monhoc():
    return db.session.query(MonHoc.ten_mon_hoc)

#Lay du lieu hoc ki
def get_hocki():
    return db.session.query(ThongTinNamHoc.hoc_ki).distinct()

#lay du lieu nam hoc
def get_namhoc():
    return db.session.query(ThongTinNamHoc.nam_hoc).distinct()

# Thống kê
def thongke_DatMon(mon=None,nam=None,hocki=None):
    query= ((((db.session.query(
        Lop.ten_lop.label('ten_lop'),
        HocSinh.id.label('id_hoc_sinh')
        ,(func.sum(Diem.so_diem * LoaiDiem.he_so) / func.sum(LoaiDiem.he_so)).label('diem_trung_binh'))
            .join(HocSinhThuocLop, HocSinhThuocLop.lop_id == Lop.id)
            .join(HocSinh, HocSinhThuocLop.hoc_sinh_id == HocSinh.id)
            .join(HocSinhHocMon, HocSinhHocMon.hoc_sinh_id == HocSinh.id)
            .join(Diem, Diem.hoc_sinh_hoc_mon_id == HocSinhHocMon.id)
            .join(LoaiDiem, Diem.loai_diem_id == LoaiDiem.id)
            .join(MonHoc, HocSinhHocMon.mon_hoc_id == MonHoc.id)
            .join(ThongTinNamHoc, HocSinhHocMon.thong_tin_nam_hoc_id == ThongTinNamHoc.id))
            .filter(MonHoc.ten_mon_hoc.__eq__(mon)))
            .filter(ThongTinNamHoc.nam_hoc.__eq__(nam)))
            .filter(ThongTinNamHoc.hoc_ki.__eq__(hocki)))
    query=query.group_by(Lop.ten_lop,HocSinh.id)
    return query.all()

#Lay cac lop da co hoc sinh
def get_hocsinh_lop():
      return (db.session.query(Lop.id,Lop.ten_lop,func.count(HocSinhThuocLop.hoc_sinh_id).label('siso'))
            .join(HocSinhThuocLop,Lop.id==HocSinhThuocLop.lop_id)
            .join(HocSinh,HocSinhThuocLop.hoc_sinh_id==HocSinh.id).group_by(Lop.id,Lop.ten_lop).distinct().all())
#Lay danh hoc sinh theo lop
def get_listHocSinh_lop(idlop):
      return ((db.session.query(HocSinh.id,HocSinh.ho,HocSinh.ten,HocSinh.gioi_tinh,HocSinh.ngay_sinh,HocSinh.dia_chi)
              .join(HocSinhThuocLop,HocSinhThuocLop.hoc_sinh_id==HocSinh.id)
              .join(Lop,HocSinhThuocLop.lop_id.__eq__(Lop.id))).filter(Lop.id.__eq__(idlop))
              .join(ThongTinNamHoc,ThongTinNamHoc.id==HocSinhThuocLop.thong_tin_nam_hoc_id).filter(ThongTinNamHoc.nam_hoc.__eq__(NamHocHienTai.NAM_HOC), ThongTinNamHoc.hoc_ki.__eq__(NamHocHienTai.HOC_KY)).all())

def get_list_class_of_teacher():
    user = GiaoVien.query.filter(GiaoVien.tai_khoan_id.__eq__(current_user.id)).first()
    return Day.query.join(Day.thong_tin_nam_hoc).join(Day.giao_vien_day_mon) \
        .filter(ThongTinNamHoc.nam_hoc.__eq__(NamHocHienTai.NAM_HOC),
                ThongTinNamHoc.hoc_ki.__eq__(NamHocHienTai.HOC_KY), GiaoVienDayMon.giao_vien_id.__eq__(user.id)) \
        .distinct(Day.lop_id).all()

def get_subject_of_teacher_in_class(class_id):
    user = GiaoVien.query.filter(GiaoVien.tai_khoan_id.__eq__(current_user.id)).first()
    list_subject = Day.query.join(Day.thong_tin_nam_hoc).join(Day.giao_vien_day_mon).join(GiaoVienDayMon.mon_hoc) \
        .filter(ThongTinNamHoc.nam_hoc.__eq__(NamHocHienTai.NAM_HOC),
                ThongTinNamHoc.hoc_ki.__eq__(NamHocHienTai.HOC_KY), Day.lop_id.__eq__(class_id),
                GiaoVienDayMon.giao_vien_id.__eq__(user.id)).all()
    return list_subject

# Kiem tra hoc sinh da co lop
def kiemtra_hocsinh_lop(id):
    return ((db.session.query(HocSinh.id,HocSinh.ho,HocSinh.ten,HocSinh.gioi_tinh,HocSinh.ngay_sinh,HocSinh.dia_chi)
              .join(HocSinhThuocLop,HocSinhThuocLop.hoc_sinh_id.__eq__(HocSinh.id))
              .join(ThongTinNamHoc,ThongTinNamHoc.id==HocSinhThuocLop.thong_tin_nam_hoc_id)
              .filter(ThongTinNamHoc.nam_hoc.__eq__(NamHocHienTai.NAM_HOC),HocSinh.id.__eq__(id)))).all()

#Lay hoc sinh
def get_hocsinh(idHocSinh):
      return (db.session.query(HocSinh.id,HocSinh.ho,HocSinh.ten,HocSinh.gioi_tinh,HocSinh.ngay_sinh,HocSinh.dia_chi)
              .filter(HocSinh.id.__eq__(idHocSinh)).first())

#Xoa hoc sinh
def delete_hocsinh(idHocSinh,idLop):
    return HocSinhThuocLop.query.filter(HocSinhThuocLop.lop_id==idLop,HocSinhThuocLop.hoc_sinh_id==idHocSinh).delete()

# def get_giaoVienDayLop():
#     return (db.session.query(Day.giao_vien_id)
#             .join(HocSinh,HocSinh.id==HocSinhHocMon.hoc_sinh_id)
#             .join(Diem,Diem.hoc_sinh_hoc_mon_id==Diem.id)
#             .join(LoaiDiem,LoaiDiem.id==Diem.loai_diem_id)
#             .join(Lop,Lop)

# def get_hoc_sinh_hoc_mon():

def luu_diem_tuong_ung(score, loai_diem, hshm_id):
    loai_diem = LoaiDiem.query.filter(LoaiDiem.loai_diem.__eq__(loai_diem)).first()
    try:
        for s in score:
                diem = Diem(so_diem=float(s), loai_diem_id=loai_diem.id, hoc_sinh_hoc_mon_id=hshm_id)
                db.session.add(diem)
                db.session.commit()
    except SQLAlchemy as e:
        print("Lớp này đã được lưu. Vui lòng nhập lớp khác")

# lưu điểm học sinh thuộc môn đó
def save_score(student_id, subject_id, score_15, score_45, score_cuoi_ky):
    ttnh = ThongTinNamHoc.query.filter(ThongTinNamHoc.nam_hoc.__eq__(NamHocHienTai.NAM_HOC), ThongTinNamHoc.hoc_ki.__eq__(NamHocHienTai.HOC_KY)).first()
    hshm = HocSinhHocMon(mon_hoc_id=subject_id, hoc_sinh_id=student_id, thong_tin_nam_hoc_id=ttnh.id)
    duplicates = HocSinhHocMon.query.filter(HocSinhHocMon.mon_hoc_id.__eq__(hshm.mon_hoc_id),
                                                                       HocSinhHocMon.hoc_sinh_id.__eq__(hshm.hoc_sinh_id),
                                                                       HocSinhHocMon.thong_tin_nam_hoc_id.__eq__(hshm.thong_tin_nam_hoc_id)).all()
    if duplicates:
        print("Lớp này đã lưu điểm")
        return {"success": "fail", "thong_bao": "Lớp này đã được lưu từ trước. Vui lòng chọn lớp khác"}
    db.session.add(hshm)
    db.session.commit()
    luu_diem_tuong_ung(score_15, "15p", hshm.id)
    luu_diem_tuong_ung(score_45, "45p", hshm.id)
    luu_diem_tuong_ung(score_cuoi_ky, "ck", hshm.id)
    return {"success": "success","thong_bao": "Đã lưu điểm thành công"}

def get_score(subject_id, student):
    ttnh = ThongTinNamHoc.query.filter(ThongTinNamHoc.nam_hoc.__eq__(NamHocHienTai.NAM_HOC),ThongTinNamHoc.hoc_ki.__eq__(NamHocHienTai.HOC_KY)).first()
    hoc_sinh_hoc_mon = HocSinhHocMon.query.filter(HocSinhHocMon.thong_tin_nam_hoc_id.__eq__(ttnh.id), HocSinhHocMon.mon_hoc_id.__eq__(subject_id), HocSinhHocMon.hoc_sinh_id.__eq__(student.id)).first()
    if not hoc_sinh_hoc_mon:
        return
    score_of_student = Diem.query.filter(Diem.hoc_sinh_hoc_mon_id.__eq__(hoc_sinh_hoc_mon.id)).all()
    test_15 = [x.so_diem for x in score_of_student if x.loai_diem.loai_diem.__eq__("15p")]
    test_45 = [x.so_diem for x in score_of_student if x.loai_diem.loai_diem.__eq__("45p")]
    test_ck = [x.so_diem for x in score_of_student if x.loai_diem.loai_diem.__eq__("ck")]
    return [test_15, test_45, test_ck]

#Lay cac nam hoc da day
def get_namhoc_giaovienday():
    user = GiaoVien.query.filter(GiaoVien.tai_khoan_id.__eq__(current_user.id)).first()
    # return ThongTinNamHoc.session.query().join(Day,Day.thong_tin_nam_hoc_id.__eq__(ThongTinNamHoc.id))
    #         .join(GiaoVien,GiaoVien.id.__eq__(user.id)).filter(Day.chu_nhiem.__eq__(True))).all()
    return (db.session.query(Day).join(ThongTinNamHoc,ThongTinNamHoc.id==Day.thong_tin_nam_hoc_id)
            .join(GiaoVienDayMon,GiaoVienDayMon.id==Day.giao_vien_day_mon_id)
            .join(GiaoVien,GiaoVienDayMon.giao_vien_id==GiaoVien.id)
            .filter(GiaoVien.tai_khoan_id.__eq__(user.id),Day.chu_nhiem.__eq__(True))).all()

#Lay lop theo nam hoc
def get_lop_namhoc(namhoc):
    user = GiaoVien.query.filter(GiaoVien.tai_khoan_id.__eq__(current_user.id)).first()
    return ((db.session.query(Day).join(Lop,Lop.id==Day.lop_id)
            .join(ThongTinNamHoc,ThongTinNamHoc.id==Day.thong_tin_nam_hoc_id))
            .join(GiaoVienDayMon,GiaoVienDayMon.id==Day.giao_vien_day_mon_id)
            .join(GiaoVien,GiaoVienDayMon.giao_vien_id==GiaoVien.id)
            .filter(ThongTinNamHoc.nam_hoc==namhoc,GiaoVien.tai_khoan_id.__eq__(user.id),Day.chu_nhiem.__eq__(True)).first())

#lay danh sach hoc sinh diem TBHK
def get_diemTB_hocKi(namhoc=None,tenlop=None):
    query = ((db.session.query(
        HocSinh.id.label("id"),
        (HocSinh.ho+" "+HocSinh.ten).label('ten_hoc_sinh'),
        Lop.ten_lop.label('ten_lop'),
        ThongTinNamHoc.hoc_ki.label('hoc_ki')
        ,(func.sum(Diem.so_diem * LoaiDiem.he_so) / func.sum(LoaiDiem.he_so)).label('diem_trung_binh')))
                .join(HocSinhThuocLop, HocSinhThuocLop.lop_id == Lop.id)
                .join(HocSinh, HocSinhThuocLop.hoc_sinh_id == HocSinh.id)
                .join(HocSinhHocMon, HocSinhHocMon.hoc_sinh_id == HocSinh.id)
                .join(Diem, Diem.hoc_sinh_hoc_mon_id == HocSinhHocMon.id)
                .join(LoaiDiem, Diem.loai_diem_id == LoaiDiem.id)
                .join(MonHoc, HocSinhHocMon.mon_hoc_id == MonHoc.id)
                .join(ThongTinNamHoc, HocSinhHocMon.thong_tin_nam_hoc_id == ThongTinNamHoc.id)
                .filter(Lop.ten_lop==tenlop,ThongTinNamHoc.nam_hoc==namhoc))
    query = query.group_by(Lop.ten_lop, HocSinh.id,ThongTinNamHoc.hoc_ki,ThongTinNamHoc.nam_hoc)
    return query.all()


# SELECT
#     lop.ten_lop AS ten_lop,
#     hoc_sinh.ten,
# --     hoc_sinh.id AS hoc_sinh_id,
#     thong_tin_nam_hoc.hoc_ki AS hoc_ki,
#     thong_tin_nam_hoc.nam_hoc AS nam_hoc,
#     SUM(diem.so_diem * loai_diem.he_so) / SUM(loai_diem.he_so) AS diem_trung_binh
# FROM
#     diem
# JOIN
#     loai_diem ON diem.loai_diem_id = loai_diem.id
# JOIN
#     hoc_sinh_hoc_mon ON diem.hoc_sinh_hoc_mon_id = hoc_sinh_hoc_mon.id
# JOIN
#     hoc_sinh ON hoc_sinh_hoc_mon.hoc_sinh_id = hoc_sinh.id
# JOIN
#     hoc_sinh_thuoc_lop ON hoc_sinh.id = hoc_sinh_thuoc_lop.hoc_sinh_id
# JOIN
#     lop ON hoc_sinh_thuoc_lop.lop_id = lop.id
# JOIN
#     mon_hoc ON hoc_sinh_hoc_mon.mon_hoc_id = mon_hoc.id
# JOIN
#     thong_tin_nam_hoc ON hoc_sinh_hoc_mon.thong_tin_nam_hoc_id = thong_tin_nam_hoc.id
#   -- Chỉ tính điểm môn Toán
# where lop.ten_lop="12A1"
# GROUP BY
#     lop.ten_lop,
#     hoc_sinh.id,
#     thong_tin_nam_hoc.hoc_ki,
#     thong_tin_nam_hoc.nam_hoc
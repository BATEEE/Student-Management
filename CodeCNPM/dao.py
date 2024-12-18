from fileinput import hook_compressed

from flask_sqlalchemy import SQLAlchemy

from models import TaiKhoan, UserRole, GiaoVien, QuanTri, MonHoc, HocSinh, HocSinhThuocLop, Lop, LoaiDiem, Diem, \
    HocSinhHocMon, ThongTinNamHoc
from init import db
from sqlalchemy import func
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

def find_student(id):
    a = HocSinhThuocLop.query.filter(HocSinhThuocLop.hoc_sinh_id.__eq__(id)).first()
    return a

def find_student_class(id):
    # Lấy đối tượng trong bảng học sinh thuộc lớp
    student = HocSinhThuocLop.query.order_by(HocSinhThuocLop.id.desc()).filter(HocSinhThuocLop.hoc_sinh_id.__eq__(id)).first()
    return Lop.query.filter(Lop.id.__eq__(student.lop_id)).first()

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


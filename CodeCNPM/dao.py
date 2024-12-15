from models import TaiKhoan, UserRole, GiaoVien, QuanTri, MonHoc, HocSinh
from init import db
import hashlib
import sys

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

def get_user_by_id(id):
    return TaiKhoan.query.get(id)

def find_student(id):
    a = HocSinh.query.filter(HocSinh.id.__eq__(id)).first()
    print(a)
    return a

def remove_student(id):
    student = a = HocSinh.query.filter(HocSinh.id.__eq__(id)).first()
    db.session.remove(student)

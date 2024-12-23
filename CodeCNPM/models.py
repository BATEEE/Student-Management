from init import db, app
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Boolean, Date, Integer, DateTime, ForeignKey, Double, Enum
from flask_login import UserMixin
from sqlalchemy.sql import func,cast
from enum import Enum as EnumRole
from flask import redirect
import hashlib
import datetime


class UserRole(EnumRole):
    GV = "GiaoVien",
    NV = "NhanVien",
    QT = "QuanTri"


# 'giao_vien.Id', 'quan_tri.Id', 'nhan_vien.Id'

class TaiKhoan(db.Model, UserMixin):
    __tablename__ = 'tai_khoan'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_tai_khoan = Column(String(45), unique=True, nullable=False)
    tai_khoan = Column(String(45), nullable=False, unique=True)
    mat_khau = Column(String(45), nullable=False)
    ngay_tao = Column(DateTime(timezone=True), default=func.now)
    email = Column(String(45), unique=True)
    user_role = Column(Enum(UserRole), default=UserRole.GV)

    # __mapper_args__ = {
    #     'polymorphic_identity': 'tai_khoan',
    #     'polymorphic_on': Id,
    #     'with_polymorphic': "*"
    # }
    giao_vien = relationship('GiaoVien', backref="tai_khoan", lazy=True)
    nhan_vien = relationship('NhanVien', backref="tai_khoan", lazy=True)
    quan_tri = relationship('QuanTri', backref="tai_khoan", lazy=True)


class HocSinh(db.Model):
    id = Column(String(10), primary_key=True)
    ho = Column(String(45), nullable=False)
    ten = Column(String(45), nullable=False)
    gioi_tinh = Column(Boolean)
    dia_chi = Column(String(100))
    email = Column(String(45))
    ngay_sinh = Column(Date)
    so_dien_thoai = Column(String(10))
    avatar = Column(String(50))
    hoc_sinh_hoc_mon = relationship('HocSinhHocMon', backref="hoc_sinh", lazy=True)
    hoc_sinh_thuoc_lop = relationship('HocSinhThuocLop', backref="hoc_sinh", lazy=True)


class GiaoVien(db.Model):
    __tablename__ = 'giao_vien'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ho = Column(String(45), nullable=False)
    ten = Column(String(45), nullable=False)
    gioi_tinh = Column(Boolean)
    dia_chi = Column(String(100))
    email = Column(String(45))
    ngay_sinh = Column(Date)
    so_dien_thoai = Column(String(10))
    day = relationship('Day', backref="giao_vien", lazy=True)
    tai_khoan_id = Column(Integer, ForeignKey('tai_khoan.id'), unique=True)

    # def __init__(self, id, ho, ten, gioi_tinh, dia_chi, email, ngay_sinh, so_dien_thoai):
    #     self.id = id
    #     self.ho = ho
    #     self.ten = ten
    #     self.gioi_tinh = gioi_tinh
    #     self.dia_chi = dia_chi
    #     self.email = email
    #     self.ngay_sinh = ngay_sinh
    #     self.so_dien_thoai = so_dien_thoai

    # __mapper_args__ = {
    #     'polymorphic_identity': 'giao_vien',
    # }


class QuanTri(db.Model):
    __tablename__ = 'quan_tri'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ho = Column(String(45), nullable=False)
    ten = Column(String(45), nullable=False)
    gioi_tinh = Column(Boolean)
    dia_chi = Column(String(100))
    email = Column(String(45))
    ngay_sinh = Column(Date)
    so_dien_thoai = Column(String(10))
    tai_khoan_id = Column(Integer, ForeignKey('tai_khoan.id'), unique=True)

    # __mapper_args__ = {
    #     'polymorphic_identity': 'quan_tri',
    # }


class NhanVien(db.Model):
    __tablename__ = 'nhan_vien'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ho = Column(String(45), nullable=False)
    ten = Column(String(45), nullable=False)
    gioi_tinh = Column(Boolean)
    dia_chi = Column(String(100))
    email = Column(String(45))
    ngay_sinh = Column(Date)
    so_dien_thoai = Column(String(10))
    tai_khoan_id = Column(Integer, ForeignKey('tai_khoan.id'), unique=True)

    def __str__(self):
        return self.ten


class Lop(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_lop = Column(String(50), nullable=False)
    khoi_lop = Column(Integer, nullable=False)
    day = relationship('Day', backref="lop", lazy=True)
    hoc_sinh_thuoc_lop = relationship('HocSinhThuocLop', backref="lop", lazy=True)


class LoaiDiem(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    loai_diem = Column(String(45), nullable=False)
    he_so = Column(Integer, nullable=False)


class MonHoc(db.Model):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    ten_mon_hoc = Column(String(50), nullable=False)
    hoc_sinh_hoc_mon = relationship('HocSinhHocMon', backref="mon_hoc", lazy=True)
    giao_vien_day_mon = relationship('GiaoVienDayMon', backref="mon_hoc", lazy=True)

    def __str__(self):
        return self.ten_mon_hoc


class ThongTinNamHoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nam_hoc = Column(String(20), nullable=False)
    hoc_ki = Column(Integer, nullable=False)
    day = relationship('Day', lazy=True)
    hoc_sinh_hoc_mon = relationship('HocSinhHocMon', backref="thong_tin_nam_hoc", lazy=True)
    hoc_sinh_thuoc_lop = relationship('HocSinhThuocLop', backref="thong_tin_nam_hoc", lazy=True)

    def __eq__(self, other):
        return self.nam_hoc > other.nam_hoc and self.hoc_ki > other.hoc_ki


class PhongHoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_phong = Column(String(45), nullable=False)
    phong = relationship('Day', backref="phong_hoc", lazy=True)


class Day(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    chu_nhiem = Column(Boolean, nullable=False)
    giao_vien_id = Column(Integer, ForeignKey('giao_vien.id'))
    lop_id = Column(Integer, ForeignKey('lop.id'))
    thong_tin_nam_hoc_id = Column(Integer, ForeignKey('thong_tin_nam_hoc.id'))
    phong_id = Column(Integer, ForeignKey('phong_hoc.id'))


class Diem(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    so_diem = Column(Double, nullable=False)
    loai_diem_id = Column(Integer, ForeignKey('loai_diem.id'), nullable=False)
    hoc_sinh_hoc_mon_id = Column(Integer, ForeignKey('hoc_sinh_hoc_mon.id'), nullable=False)


class HocSinhHocMon(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    mon_hoc_id = Column(Integer, ForeignKey('mon_hoc.id'), nullable=False)
    hoc_sinh_id = Column(String(10), ForeignKey('hoc_sinh.id'), nullable=False)
    thong_tin_nam_hoc_id = Column(Integer, ForeignKey('thong_tin_nam_hoc.id'), nullable=False)
    diem = relationship('Diem', backref="hoc_sinh_hoc_mon", lazy=True)


class HocSinhThuocLop(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    hoc_sinh_id = Column(String(10), ForeignKey('hoc_sinh.id'), nullable=False)
    lop_id = Column(Integer, ForeignKey('lop.id'), nullable=False)
    thong_tin_nam_hoc_id = Column(Integer, ForeignKey('thong_tin_nam_hoc.id'), nullable=False)


class GiaoVienDayMon(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    mon_hoc_id = Column(Integer, ForeignKey('mon_hoc.id'), nullable=False)
    giao_vien_id = Column(Integer, ForeignKey('giao_vien.id'), nullable=False)

class QuyDinh:
    SI_SO = 40
    AGE_MAX = 20
    AGE_MIN = 15

class NamHocHienTai:
    NAM_HOC = "2024"
    HOC_KY = 1

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Tạo tài khoản Quản trị viên
        taikhoan1 = TaiKhoan(
            ten_tai_khoan="Trần Tuấn Thắng",
            tai_khoan="admin1",
            mat_khau=str(hashlib.md5("123456".strip().encode('utf-8')).hexdigest()),
            ngay_tao="2004-2-12",
            email="thangancut@gmail.com",
            user_role=UserRole.QT
        )

        # Tạo tài khoản Nhân viên
        taikhoan2 = TaiKhoan(
            ten_tai_khoan="Nguyễn Hoàng Phúc",
            tai_khoan="nhanvien1",
            mat_khau=str(hashlib.md5("123456".strip().encode('utf-8')).hexdigest()),
            ngay_tao="2004-12-15",
            email="phuc@gmail.com",
            user_role=UserRole.NV
        )

        # Tạo tài khoản Giáo viên
        taikhoan3 = TaiKhoan(
            ten_tai_khoan="Lê Minh Tuấn",
            tai_khoan="giaovien1",
            mat_khau=str(hashlib.md5("123456".strip().encode('utf-8')).hexdigest()),
            ngay_tao="2005-7-18",
            email="tuanlminh@gmail.com",
            user_role=UserRole.GV
        )

        # Tạo Quản trị viên
        quantri = QuanTri(
            ho="Trần Tuấn",
            ten='Thắng',
            gioi_tinh=0,
            dia_chi="189/34/28A Bach Dang Phuong 3 Go Vap",
            email="thangdaubuoi@gmail.com",
            ngay_sinh="2004-3-20",
            so_dien_thoai="01242542",
            tai_khoan_id=taikhoan1.id
        )

        # Tạo Nhân viên
        nv = NhanVien(
            ho='Nguyễn Hoàng',
            ten='Phúc',
            gioi_tinh=0,
            dia_chi='189/34/28A Bach Dang Phuong 3 Go Vap',
            email="phuc@gmail.com",
            ngay_sinh="2004-12-31",
            so_dien_thoai="01242542",
            tai_khoan_id=taikhoan2.id
        )

        # Tạo Giáo viên
        giaovien = GiaoVien(
            ho="Lê Minh",
            ten="Tuấn",
            gioi_tinh=0,
            dia_chi="12/1 Nguyen Thi Minh Khai, TP HCM",
            email="tuanlminh@gmail.com",
            ngay_sinh="1990-6-15",
            so_dien_thoai="0987555577",
            tai_khoan_id=taikhoan3.id
        )

        # Tạo Môn học
        mon_hoc = MonHoc(
            ten_mon_hoc="Lập trình Python"
        )

        # Tạo Lớp học
        lop1 = Lop(
            ten_lop="Lớp 12A1",
            khoi_lop=12
        )

        # Tạo Học sinh
        hoc_sinh1 = HocSinh(
            id="HS0001",
            ho="Nguyễn",
            ten="Minh",
            gioi_tinh=True,
            dia_chi="TP HCM",
            email="minh@gmail.com",
            ngay_sinh="2006-8-25",
            so_dien_thoai="0932383878",
            avatar="avatar1.jpg"
        )

        hoc_sinh2 = HocSinh(
            id="HS0002",
            ho="Trần",
            ten="An",
            gioi_tinh=True,
            dia_chi="Đà Nẵng",
            email="an@gmail.com",
            ngay_sinh="2007-10-12",
            so_dien_thoai="0977654321",
            avatar="avatar2.jpg"
        )

        # Tạo Mối quan hệ Học sinh thuộc lớp
        hoc_sinh_thuoc_lop1 = HocSinhThuocLop(
            hoc_sinh_id=hoc_sinh1.id,
            lop_id=lop1.id,
            thong_tin_nam_hoc_id=1
        )

        hoc_sinh_thuoc_lop2 = HocSinhThuocLop(
            hoc_sinh_id="HS0002",
            lop_id=lop1.id,
            thong_tin_nam_hoc_id=1
        )

        # Thêm tất cả vào session và commit
        db.session.add_all([lop1, mon_hoc, hoc_sinh1, hoc_sinh2])
        db.session.commit()
        db.session.add_all([taikhoan1, taikhoan2, taikhoan3])
        db.session.commit()
        db.session.add_all([hoc_sinh_thuoc_lop1, hoc_sinh_thuoc_lop2, quantri, nv, giaovien])
        db.session.commit()
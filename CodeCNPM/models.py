from turtledemo.penrose import start

from sqlalchemy.dialects.mysql import DECIMAL

from init import db, app
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Boolean, Date, Integer, DateTime, ForeignKey, Double, Enum
from flask_login import UserMixin
from sqlalchemy.sql import func, cast
from enum import Enum as EnumRole
from flask import redirect
import hashlib
import datetime
from datetime import date


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
    ngay_tao = Column(DateTime(timezone=True))
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

    def __str__(self):
        return self.ten_tai_khoan


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
    tai_khoan_id = Column(Integer, ForeignKey('tai_khoan.id'), unique=True)
    def __str__(self):
        return self.ho+" "+self.ten
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
    def __str__(self):
        return self.ho+" "+self.ten
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
        return self.ho+" "+self.ten


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
    diem = relationship('Diem', backref="loai_diem", lazy=True)


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
    day = relationship('Day', backref="thong_tin_nam_hoc", lazy=True)
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
    giao_vien_day_mon_id = Column(Integer, ForeignKey('giao_vien_day_mon.id'))
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
    day = relationship('Day', backref="giao_vien_day_mon", lazy=True)


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
        nam_hoc_1 = ThongTinNamHoc(nam_hoc="2023-2024", hoc_ki=1)
        nam_hoc_2 = ThongTinNamHoc(nam_hoc="2023-2024", hoc_ki=2)
        db.session.add_all([nam_hoc_1, nam_hoc_2])

        # Thêm dữ liệu vào bảng Lớp
        lop_1 = Lop(ten_lop="12A1", khoi_lop=12)
        lop_2 = Lop(ten_lop="12A2", khoi_lop=12)
        db.session.add_all([lop_1, lop_2])

        # Thêm dữ liệu vào bảng Phòng học
        phong_1 = PhongHoc(ten_phong="Phòng 101")
        phong_2 = PhongHoc(ten_phong="Phòng 102")
        db.session.add_all([phong_1, phong_2])

        # Thêm dữ liệu vào bảng Môn học
        mon_toan = MonHoc(ten_mon_hoc="Toán")
        mon_ly = MonHoc(ten_mon_hoc="Vật Lý")
        mon_hoa = MonHoc(ten_mon_hoc="Hóa Học")
        db.session.add_all([mon_toan, mon_ly, mon_hoa])

        # Thêm dữ liệu vào bảng Loại điểm
        loai_diem_1 = LoaiDiem(loai_diem="Kiểm tra miệng", he_so=1)
        loai_diem_2 = LoaiDiem(loai_diem="Kiểm tra 15 phút", he_so=1)
        loai_diem_3 = LoaiDiem(loai_diem="Kiểm tra 1 tiết", he_so=2)
        loai_diem_4 = LoaiDiem(loai_diem="Điểm thi", he_so=3)
        db.session.add_all([loai_diem_1, loai_diem_2, loai_diem_3, loai_diem_4])

        # Thêm dữ liệu vào bảng Giáo viên
        gv_1 = GiaoVien(
            ho="Nguyễn", ten="Văn A", gioi_tinh=True, dia_chi="Hà Nội", email="nguyenvana@gmail.com",
            ngay_sinh=date(1980, 5, 20), so_dien_thoai="0987654321", tai_khoan_id=None
        )
        gv_2 = GiaoVien(
            ho="Trần", ten="Thị B", gioi_tinh=False, dia_chi="Hồ Chí Minh", email="tranthib@gmail.com",
            ngay_sinh=date(1985, 8, 15), so_dien_thoai="0981234567", tai_khoan_id=None
        )
        db.session.add_all([gv_1, gv_2])

        tk_1 = TaiKhoan(
            ten_tai_khoan="giaovien_a", tai_khoan="giaovien_a", mat_khau="123456", email="nguyenvana@gmail.com",
            user_role=UserRole.GV
        )
        tk_2 = TaiKhoan(
            ten_tai_khoan="giaovien_b", tai_khoan="giaovien_b", mat_khau="123456", email="tranthib@gmail.com",
            user_role=UserRole.GV
        )
        db.session.add_all([tk_1, tk_2])

        # Thêm dữ liệu vào bảng Học sinh
        hs_1 = HocSinh(
            id="HS001", ho="Lê", ten="Văn C", gioi_tinh=True, dia_chi="Đà Nẵng", email="levanc@gmail.com",
            ngay_sinh=date(2006, 9, 12), so_dien_thoai="0908765432", avatar="avatar1.png"
        )
        hs_2 = HocSinh(
            id="HS002", ho="Phạm", ten="Thị D", gioi_tinh=False, dia_chi="Hải Phòng", email="phamthid@gmail.com",
            ngay_sinh=date(2006, 11, 5), so_dien_thoai="0912345678", avatar="avatar2.png"
        )
        db.session.add_all([hs_1, hs_2])

        # Thêm dữ liệu vào bảng Học sinh học môn
        # hshm_1 = HocSinhHocMon(mon_hoc_id=1, hoc_sinh_id="HS001", thong_tin_nam_hoc_id=1)
        # hshm_2 = HocSinhHocMon(mon_hoc_id=2, hoc_sinh_id="HS002", thong_tin_nam_hoc_id=2)
        # db.session.add_all([hshm_1, hshm_2])

        # Thêm dữ liệu vào bảng Giao viên dạy môn
        # gv_dm_1 = GiaoVienDayMon(mon_hoc_id=1, giao_vien_id=1)
        # gv_dm_2 = GiaoVienDayMon(mon_hoc_id=2, giao_vien_id=2)
        # db.session.add_all([gv_dm_1, gv_dm_2])

        # Thêm dữ liệu vào bảng Điểm
        # diem_1 = Diem(so_diem=8.5, loai_diem_id=1, hoc_sinh_hoc_mon_id=1)
        # diem_2 = Diem(so_diem=9.0, loai_diem_id=3, hoc_sinh_hoc_mon_id=2)
        # db.session.add_all([diem_1, diem_2])

        # Lưu thay đổi
        db.session.commit()
        tk_qt = TaiKhoan(
        ten_tai_khoan="quantri_01", tai_khoan="quantri_01", mat_khau="admin123", email="admin01@gmail.com",
        user_role=UserRole.QT
        )
        db.session.add(tk_qt)

    # Thêm dữ liệu vào bảng Quản trị
        qt_1 = QuanTri(
        ho="Trần", ten="Quản Trị", gioi_tinh=True, dia_chi="Hồ Chí Minh", email="admin01@gmail.com",
        ngay_sinh=date(1985, 8, 15), so_dien_thoai="0912345678", tai_khoan_id=tk_qt.id
        )
        db.session.add(qt_1)

    # Thêm dữ liệu vào bảng Tài khoản Nhân viên
        tk_nv = TaiKhoan(
        ten_tai_khoan="nhanvien_01", tai_khoan="nhanvien_01", mat_khau="nv123456", email="nhanvien01@gmail.com",
        user_role=UserRole.NV
        )
        db.session.add(tk_nv)

    # Thêm dữ liệu vào bảng Nhân viên
        nv_1 = NhanVien(
        ho="Lê", ten="Nhân Viên", gioi_tinh=False, dia_chi="Đà Nẵng", email="nhanvien01@gmail.com",
        ngay_sinh=date(1990, 3, 10), so_dien_thoai="0981122334", tai_khoan_id=tk_nv.id
        )
        db.session.add(nv_1)

    # Lưu thay đổi
        db.session.commit()

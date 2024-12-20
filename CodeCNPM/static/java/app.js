let currentchar=null

const toggleButton = document.getElementById('toggle-btn')
const sidebar = document.getElementById('sidebar')
function toggleSidebar() {
    sidebar.classList.toggle('close')
    toggleButton.classList.toggle('rotate')

    Array.from(sidebar.getElementsByClassName('show')).forEach(ul => {
        ul.classList.remove('show');
        ul.previousElementSibling.classList.remove('rotate');
    });    
}


function toggleSubmenu(button) {
    button.nextElementSibling.classList.toggle('show')
    button.classList.toggle('rotate')

    if(sidebar.classList.contains('close')) {
        sidebar.classList.toggle('close')
        toggleButton.classList.toggle('rotate')
    }
}

//login
// Ẩn hiện mật khẩu
document.addEventListener("DOMContentLoaded", function () {
    const eyeOffIcons = document.querySelectorAll('ion-icon[name="eye-off-outline"]');
    const eyeIcons = document.querySelectorAll('ion-icon[name="eye-outline"]');
    const passwordInputs = document.querySelectorAll('input[type="password"]');
  
    eyeOffIcons.forEach((eyeOffIcon, index) => {
      eyeOffIcon.addEventListener("click", function () {
        passwordInputs[index].type = "text";
        eyeOffIcon.style.display = "none";
        eyeIcons[index].style.display = "block";
      });
    });
  
    eyeIcons.forEach((eyeIcon, index) => {
      eyeIcon.addEventListener("click", function () {
        passwordInputs[index].type = "password";
        eyeOffIcons[index].style.display = "block";
        eyeIcon.style.display = "none";
      })
    })
})


//edit-student

function toggleEditStudent() {
        const inputFields = document.querySelectorAll(".editInput");
        const selectFields = document.querySelectorAll(".editSelect");

        inputFields.forEach(input => {
            if (input.hasAttribute("readonly")) {
                input.removeAttribute("readonly");
            }
        })

        selectFields.forEach(select => {
            if (select.hasAttribute("disabled")) {
                select.removeAttribute("disabled");
            }
        })
    }

//Load hoc ki
function loadHocKi() {
    const namHoc = document.getElementById("namhoc_select").value;

    fetch(`/admin/get_hocki?nam_hoc=${namHoc}`)
        .then(res => res.json())
        .then(data => {
            let hocKiSelect = document.getElementById("hocki_select");
            hocKiSelect.innerHTML = "<option disabled selected>Chọn học kì</option>";
            data.forEach(hoc_ki => {
                let option = document.createElement("option");
                option.value = hoc_ki;
                option.text = `${hoc_ki}`;
                hocKiSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error:', error));
}

function updateTableUI(data) {
    let row = document.getElementById("rows");
    let tr = document.createElement('tr')

    let td_id = document.createElement('td')
    td_id.textContent = data.id

    let td_name = document.createElement('td')
    td_name.textContent = data.name

    let td_sex = document.createElement('td')
    td_sex.textContent = data.sex

    let td_year = document.createElement('td')
    td_year.textContent = data.year

    let td_address = document.createElement('td')
    td_address.textContent = data.address

    row.appendChild(tr)
    tr.appendChild(td_id)
    tr.appendChild(td_name)
    tr.appendChild(td_sex)
    tr.appendChild(td_year)
    tr.appendChild(td_address)
}

function addToTable() {
    number_of_class = document.getElementById('number_of_class')?.value
    class_id = document.getElementById('class')?.value
    if (!number_of_class || !class_id) {
        console.error("Missing input values");
        return; // Dừng hàm nếu thiếu dữ liệu
    }
        console.log(`/nv/create_class?class_id=${class_id}&number_of_class=${number_of_class}`)
    fetch(`/nv/create_class?class_id=${class_id}&number_of_class=${number_of_class}`, {
        method: "GET",
//        body: JSON.stringify({
//            id: 'id',
//            name: 'name',
//            sex: 'sex',
//            year: 'year',
//            address: 'address'
//        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.log(data)
        updateTableUI(data);
    }).catch(error => {
        console.error("Fetch error:", error);
    });
}

// xóa học sinh khỏi bảng danh sách lớp
function deleteStudentFromTable(id) {
    if (confirm("Bạn chắc chắn xóa không?") === true) {
        fetch(`/api/create_class/${id}`, {
            method: "delete"
        }).then(res => res.json()).then(data => {
            alert(data.message)
            document.getElementById(`Student${id}`).style.display = "none";

        }).catch(error => {
            alert("Có lỗi xảy ra. Vui lòng thử lại.");
        });
    }
}

function deleteStudentFromTableNoConfirm(id) {
        fetch(`/api/create_class/${id}`, {
            method: "delete"
        }).then(res => res.json()).then(data => {
            document.getElementById(`Student${id}`).style.display = "none";

        }).catch(error => {
            alert("Có lỗi xảy ra. Vui lòng thử lại.");
        });
}

function deleteAllStudentFromTable() {
    if (confirm("Bạn chắc chắn xóa không?") === true) {
        row = document.getElementById('rows')
        rows = row.querySelectorAll('tr')
        rows.forEach(item => {
            id = item.querySelector('td').textContent
            console.log(id)
            deleteStudentFromTableNoConfirm(id)
        })
    }
}


//function addStudentToTable() {
//    class_id = document.getElementById('class_id')
//    number_of_class = document.getElementById('number_of_class')
//    fetch(`/nv/create_class?class_id=${class_id}&number_of_class=${number_of_class})`,{
//        method: 'POST',
//        headers: {
//            'Content-Type': 'application/json',
//        }
//    })
//    .then(response => response.json())
//    .then(data => {
//         row = document.getElementById('rows')
//         console.log(data)
//         if(data) {
//            data.forEach(item -> {
//                a = "<tr id='{{i.id}}'> <td>{{i.id}}</td><td>{{i.ho + " " + i.ten}}</td><td>{{'Nam' if i.gioi_tinh == 0 else 'Nữ'}}</td><td>{{i.ngay_sinh.year}}</td><td>{{i.dia_chi}}</td><td class='delete-student'><button class='btn-delete' type='button' onclick='deleteStudentFromTable({{i.id}})'>x</button></td></tr>"
//
//            })
//         }
//     });
//}
//         else {
//            const tr = document.createElement('tr');
//            const td = document.createElement('td');
//            td.setAttribute('colspan', '5');
//            td.textContent = 'Không có dữ liệu thống kê.';
//            tr.appendChild(td);
//            tbody.appendChild(tr);
//            }
//            })
//    .catch(error => {
//        console.error('Error:', error);
//    });
//}


//add_student_table


// Thêm học sinh vào danh sách lớp
function AddStudentFunc() {
    addContainer = document.querySelector('.add-into-list')
    addButton = document.getElementById('add-button')
    addContainer.classList.toggle('toggle-block')

    if (addContainer.classList.contains('toggle-block')) {
        addButton.style.filter = 'brightness(50%)';
        addButton.style.pointerEvents = 'none';
    } else {
        addButton.style.filter = 'brightness(100%)';
        addButton.style.pointerEvents = 'auto';
    }
}
//Điều chỉnh danh lớp
let dem=1
let selectedStudents = [];
document.addEventListener('DOMContentLoaded',()=>{
    if (window.location.pathname === '/nv/adjust_class') {

    loadSiSo();
}
})

//Xóa học sinh khỏi lớp UI
function delete_hocSinhUI(id,class_id){
     if(selectedStudents.find(student => student.id === id && student.id_class === class_id))
        selectedStudents=selectedStudents.filter(student=> student.id!==id && student.id_class!==class_id)
     if (confirm("Bạn chắc chắn xóa không?") === true) {
        fetch(`/api/adjust_class/${id}&${class_id}`, {
            method: "delete"
        }).then(res => res.json()).then(data => {
            alert(data.message)
            document.getElementById(`studentId${id}`).style.display = "none";
        }).catch(error => {
            alert("Có lỗi xảy ra. Vui lòng thử lại.");
        });
    }
}


function loadSiSo(){
    dem=1
    const selectElement=document.getElementById('class')
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    const siSo=selectedOption.getAttribute("data-siso");
    const updateSiSo=document.getElementById('siso')
    updateSiSo.value=siSo
    const idLop = selectElement.options[selectElement.selectedIndex].id;

    fetch(`/nv/adjust_class/get_listStudent?id_lop=${idLop}`,{
    method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
        })
        .then(res => res.json())
        .then(data => {
            if(data)
            {
            const rowStudent=document.getElementById('hocsinh')
            rowStudent.innerHTML=""
            data.forEach(item =>{

            const tr = document.createElement('tr');
            tr.setAttribute('id','studentId'+item.id)
            const tdStt = document.createElement('td');
            const tdHoTen = document.createElement('td');
            const tdGioiTinh = document.createElement('td');
            const tdNgaySinh = document.createElement('td');
            const tdDiaChi=document.createElement('td')

            tdStt.textContent=dem++
            tdHoTen.textContent=item.ho+" "+item.ten
            tdGioiTinh.textContent=item.gioi_tinh ? "Nữ" : "Nam"
            tdNgaySinh.textContent=item.ngay_sinh
            tdDiaChi.textContent=item.dia_chi

            tr.appendChild(tdStt)
            tr.appendChild(tdHoTen)
            tr.appendChild(tdGioiTinh)
            tr.appendChild(tdNgaySinh)
            tr.appendChild(tdDiaChi);

            let tdElement = document.createElement('td');
            tdElement.classList.add('delete-student');
            tdElement.setAttribute('id',item.id)
            let buttonElement = document.createElement('button');
            buttonElement.setAttribute('type', 'submit');
            buttonElement.textContent = 'x';

            buttonElement.setAttribute('id',item.id)
            buttonElement.addEventListener('click',function (){
            delete_hocSinhUI(item.id,idLop)
            })

            tdElement.appendChild(buttonElement);
            tr.appendChild(tdElement)
            rowStudent.appendChild(tr)
            })
            }
        })
        .catch(error => console.error('Error:', error));
}
//
function updateAdjustTable(){
            const tr = document.createElement('tr');
            const tdStt = document.createElement('td');
            const tdHoTen = document.createElement('td');
            const tdGioiTinh = document.createElement('td');
            const tdNgaySinh = document.createElement('td');
            const tdDiaChi=document.createElement('td')

            tdStt.textContent=dem++
            tdHoTen.textContent=item.ho+" "+item.ten
            tdGioiTinh.textContent=item.gioi_tinh ? "Nữ" : "Nam"
            tdNgaySinh.textContent=item.ngay_sinh
            tdDiaChi.textContent=item.dia_chi
            tr.appendChild(tdStt)
            tr.appendChild(tdHoTen)
            tr.appendChild(tdGioiTinh)
            tr.appendChild(tdNgaySinh)
            tr.appendChild(tdDiaChi);
            let tdElement = document.createElement('td');
            tdElement.classList.add('delete-student');
            let buttonElement = document.createElement('button');
            buttonElement.setAttribute('type', 'submit');
            buttonElement.textContent = 'x';
            tdElement.appendChild(buttonElement);
            tr.appendChild(tdElement)
}

function AddStudentToTable() {
    var studentId = document.getElementById('student_id').value;
    var selectElement=document.getElementById('class');
    var classId = selectElement.options[selectElement.selectedIndex].id;
    if (studentId && classId) {
        fetch(`/nv/adjust_class/get_hocSinh?student_id=${studentId}&class_id=${classId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if ((Array.isArray(data) && data.length === 0)) {
               alert("Lỗi đã có học sinh này trong lớp hoặc nhập sai id!")
               return
            }
            if (selectedStudents.find(student => student.id === data["id"] && student.id_class === classId)) {
            alert("Học sinh này đã được thêm: " + data["ho_ten"]);
            return;
               }
            const rowStudent=document.getElementById('hocsinh')
            const tr = document.createElement('tr');
            tr.setAttribute('id','studentId'+data["id"])
            const tdStt = document.createElement('td');
            const tdHoTen = document.createElement('td');
            const tdGioiTinh = document.createElement('td');
            const tdNgaySinh = document.createElement('td');
            const tdDiaChi=document.createElement('td')

            tdStt.textContent=dem++
            tdHoTen.textContent=data["ho_ten"]
            tdGioiTinh.textContent=data["gioi_tinh"]
            tdNgaySinh.textContent=data["ngay_sinh"]
            tdDiaChi.textContent=data["dia_chi"]

            tr.appendChild(tdStt)
            tr.appendChild(tdHoTen)
            tr.appendChild(tdGioiTinh)
            tr.appendChild(tdNgaySinh)
            tr.appendChild(tdDiaChi);

            let tdElement = document.createElement('td');
            tdElement.classList.add('delete-student');
            let buttonElement = document.createElement('button');
            buttonElement.setAttribute('type', 'submit');
            buttonElement.textContent = 'x';

            //gan id va bat su kien click
            buttonElement.setAttribute('id',data["id"])
            buttonElement.addEventListener('click',function (){
            console.log(data["id"])
            delete_hocSinhUI(data["id"],classId)
            })

            tdElement.appendChild(buttonElement);
            tr.appendChild(tdElement)
            rowStudent.appendChild(tr)
            selectedStudents.push({
            "id":data["id"],
            "id_class":classId
            })
        })
        .catch(error => {
            console.error('Lỗi:', error);
        });
    } else {
        alert('Vui lòng nhập ID học sinh!');
    }
}

function AddStudentList() {
    if (Array.isArray(selectedStudents) && selectedStudents.length !== 0) {
        fetch(`/nv/adjust_class`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
               students:selectedStudents
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                selectedStudents=[]
            } else {
                alert('Lỗi: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Lỗi:', error);
        });
    } else {
        alert('Vui lòng thực hiện thay đổi!');
    }
}


//Nhập input cho điểm
function limitInput() {
  var inputs = document.querySelectorAll('.scoreInput');

  // Duyệt qua từng input
  inputs.forEach(function(input) {
    var value = input.value;

    // Kiểm tra xem giá trị có phải là số và có tối đa 2 chữ số
    if (/^\d{1,2}$/.test(value)) {
      // Cắt nếu giá trị vượt quá 10
      if (value > 10) {
        input.value = "10";
      }
    } else {
      // Nếu không phải là số hợp lệ, chỉ giữ lại phần số
      input.value = value.replace(/[^0-9]/g, '').slice(0, 2);
    }
  });
}

// Thống kê
let char=null

function thongke(){
    const mon=document.getElementById('monhoc_select').value;
    const nam=document.getElementById('namhoc_select').value;
    const hocki=document.getElementById('hocki_select').value;
        if (mon === "default" || nam === "default" || hocki === "Chọn học kì") {
            alert("Vui lòng chọn dầy đủ năm học, học kì, môn học!")
            return
        }
    fetch(`/admin/get_thongke?nam_hoc=${nam}&hoc_ki=${hocki}&mon_hoc=${mon}`,{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('thongke_datmon');
        tbody.innerHTML ='';
        if (data) {
            const stt=document.createElement('td')
            const soluongdat=document.createElement('td')
            const tile=document.createElement('td')
            const lop = {};
            for (let item of data){
             const tenlop = item.ten_lop;
             const diem=item.diem_trung_binh;
            if (!lop[tenlop]) {
            lop[tenlop]={
            SiSo:0,
            Dat:0
            }
            }
            lop[tenlop].SiSo++;
            if (diem>=5)
            lop[tenlop].Dat++
        }
           let count=1;
            let dt=[]
            let labels=[]
         for (let item in lop) {
                const tr = document.createElement('tr');
                const tdSTT = document.createElement('td');
                const tdTenLop = document.createElement('td');
                const tdSiSo = document.createElement('td');
                const tdDat = document.createElement('td');
                const tdTiLeDat=document.createElement('td')
                tdSTT.textContent=count++;
                tdTenLop.textContent=item
                tdSiSo.textContent=lop[item].SiSo
                tdDat.textContent=lop[item].Dat
                const tile=((lop[item].Dat/lop[item].SiSo)*100)
                tdTiLeDat.textContent=tile.toFixed(2) + "%"
                tr.appendChild(tdSTT);
                tr.appendChild(tdTenLop);
                tr.appendChild(tdSiSo);
                tr.appendChild(tdDat);
                tr.appendChild(tdTiLeDat);
                tbody.appendChild(tr);
                dt.push(tile)
                labels.push(item)

            }
         const ctx = document.getElementById('myChart').getContext('2d');
         if(char){
         char.destroy()
         }
          char=new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: '# Tỉ lệ đạt',
            data:dt,
            borderWidth: 1,
            backgroundColor: ['red', 'green', 'blue', 'gold', 'brown']
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
              min:0,
              max:100,
              ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }

            }
          }
        }
      });
}
         else {
            const tr = document.createElement('tr');
            const td = document.createElement('td');
            td.setAttribute('colspan', '5');
            td.textContent = 'Không có dữ liệu thống kê.';
            tr.appendChild(td);
            tbody.appendChild(tr);
            }
            })
    .catch(error => {
        console.error('Error:', error);
    });
}


// Thông báo thêm học sinh
function thongBaoThemHocSinh(msg) {
//    if (msg !== "") {
//        alert(msg)
//    }
    console.log(1)
}

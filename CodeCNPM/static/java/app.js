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

function AddStudentList() {
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



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


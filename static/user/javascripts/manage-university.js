var logined = $('#user-authenticated').attr('logined');
var current_user = $('#user-menu').attr('user-id');
var university;
$(document).ready(function () {
    if (logined == 'true') {
        get_manage_universities(current_user);
    }
    $(document).on('click', '.sector-manage', function() {
        let university_id = $(this).attr('university-id');
        let university_name = $(this).attr('university-name');
        university = university_id;
        $('.modal-uname').text(university_name);
        get_university_sectors(university_id);
        get_university_unasign_sectors(university_id);
    });
    $("#add-sector-form").submit(function (e) {
        e.preventDefault();
        let csrftoken = getCookie("csrftoken");
        let data = $(this).serializeArray();
        data.push({
            name: "university",
            value: university
        });
        data.push({
            name: "csrfmiddlewaretoken",
            value: csrftoken
        });
        console.log(data);
        let url = "/api/v1/edit/manage/add-university-sector";
        ajax_request(false, true, "POST", "json", url, null, data, add_sector_success_callback, error_callback);
    });
});

function add_sector_success_callback(response) {
    let result = response;
    if(result.success) {
        toastr.success(`Bạn đã thêm thành công nhóm ngành "${result.sector}" vào "${result.university}"`);
        get_university_sectors(university);
        get_university_unasign_sectors(university);
    }
    else {
        let error = '';
        if (result.code === "universitydoesnotexist") {
            error = `Trường này không tồn tại!`;
        }
        else if(result.code === "sectordoesnotexist") {
            error = `Nhóm ngành này không tồn tại`;
        }
        else error = "Không thể sửa nhóm ngành này. Bạn hãy kiểm tra lại !";
        toastr.error(error);
    }
}

function get_manage_universities(user_id) {
    let url = `/api/v1/user/manage?user=${user_id}`;
    ajax_request(false, true, "GET", "json", url, null, null, manage_universities_success_callback, error_callback);
}

function manage_universities_success_callback(response) {
    let universities = response.manage_universities;
    let inner = '';
    universities.forEach(university => {
        inner += `<div class="m-widget4__item animated bounceInRight">
                        <div class="m-widget4__img m-widget4__img--pic">
                            <img src="../../../static/share/images/vnu_avatar.jpg" alt="">
                        </div>
                        <div class="m-widget4__info">
                            <span class="m-widget4__title">
								${university.name}
                           </span>
                            <br>
                            <span class="m-widget4__sub">
                                <a href="${university.site_href}" target="_blank"><i>Thông tin trường ...</i></a>
                            </span>
                        </div>
                        <div class="btn-group">
                            <span><button href="#" class="m-btn m-btn--pill m-btn--hover-info btn btn-sm btn-secondary mx-2 sector-manage" university-id="${university.id}" university-name="${university.name}" data-toggle="modal" data-target="#sector-modal">Quản lý nhóm ngành</button></span>                        	
                            <span><button href="#" class="m-btn m-btn--pill m-btn--hover-accent btn btn-sm btn-secondary" university-id="${university.id}" university-name="${university.name}" data-toggle="modal" data-target="#score-modal">Quản lý điểm</button></span>
						</div>
                    </div>`;
        // $('.m-widget4').append(inner);
    });
    $('.m-widget4').empty().html(inner);
}

function get_university_sectors(university) {
    let url = `/api/v1/sectors?university=${university}`;
    ajax_request(false, true, "GET", 'json', url, null, null, university_sectors_success_callback, error_callback);
}

function university_sectors_success_callback(response) {
    let sectors = response.sectors;
    let inner = '';
    let sectors_length = sectors.length;
    sectors.forEach((sector, index) => {
        let name = capitalize(sector.name.toLowerCase());
        let reverse_name = capitalize(sectors[sectors_length - index -1].name.toLowerCase());
        // console.log(reverse_name);
        inner += `<div class="col-12 px-0 my-2 animated bounceInRight"><i class="la la-angle-double-right"></i> ${reverse_name}</div>`;
    });
    $('#current-sectors').empty().html(inner);
}

function get_university_unasign_sectors(university) {
    let url = `/api/v1/unasign-sectors?university=${university}`;
    ajax_request(false, true, "GET", 'json', url, null, null, university_unasign_sectors_success_callback, error_callback);
}

function university_unasign_sectors_success_callback(response) {
    let sectors = response.sectors;
    let inner = "";
    sectors.forEach((sector, index) => {
        let name = capitalize(sector.name.toLowerCase());
        // console.log(reverse_name);
        inner += `<option value="${sector.id}"><i class="la la-angle-double-right"></i> ${name}</option>`;
    });
    $('#add-sector-options').empty().html(inner);
}

function error_callback(response) {
    alert("Đã xảy ra lỗi, xem response tại console !!")
}
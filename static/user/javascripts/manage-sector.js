$(document).ready(function () {
    let remove_sector;
    let logined = $('#user-authenticated').attr('logined');
    if(logined == 'true') {
        get_all_sectors();
    }
    $("#add-sector").submit(function (e) {
        e.preventDefault();
        let csrftoken = getCookie("csrftoken");
        let data = $(this).serializeArray();
        data.push({
            name: "csrfmiddlewaretoken",
            value: csrftoken
        });
        let url = "/api/v1/edit/sector/add_sector";
        ajax_request(false, true, "POST", "json", url, null, data, add_sector_success_callback, error_callback);
    });

    $("#edit-sector").submit(function (e) {
        e.preventDefault();
        let csrftoken = getCookie("csrftoken");
        let data = $(this).serializeArray();
        data.push({
            name: "csrfmiddlewaretoken",
            value: csrftoken
        });
        let url = "/api/v1/edit/sector/update_sector";
        ajax_request(false, true, "POST", "json", url, null, data, update_sector_success_callback, error_callback);
    });

    $(document).on('click', '.sector-remove-btn', function () {
        remove_sector = $(this).attr('sector-id');
        let name = $(this).attr('sector-name');
        let confirm_inner = `<li>${name}</li>`;
        $('#sector-remove-checked').empty().html(confirm_inner);
    });
    $(document).on('click', '#confirmed-remove-btn', function () {
        let csrftoken = getCookie("csrftoken");
        let data = [{
           name: "sector_id",
           value: remove_sector
        }];
        data.push({
            name: "csrfmiddlewaretoken",
            value: csrftoken
        });
        let url = "/api/v1/edit/sector/remove_sector";
        ajax_request(false, true, "POST", "json", url, null, data, remove_sector_success_callback, error_callback);
    })
});

function add_sector_success_callback(response) {
    let result = response;
    if (result.success === true) {
        toastr.success(`Bạn đã thêm thành công nhóm ngành "${result.name}"`);
        get_all_sectors();
    }
    else {
        let error = '';
        if (result.code === "already") {
            error = `Nhóm ngành này đã tồn tại!`;
        }
        else error = "Không thể thêm nhóm ngành này. Bạn hãy kiểm tra lại !";
        toastr.error(error);
    }
}

function update_sector_success_callback(response) {
    let result = response;
    if (result.success === true) {
        toastr.success(`Bạn đã sửa thành công nhóm ngành "${result.old}" thành "${result.new}"`);
        get_all_sectors();
    }
    else {
        let error = '';
        if (result.code === "already") {
            error = `Nhóm ngành này đã tồn tại!`;
        }
        else error = "Không thể sửa nhóm ngành này. Bạn hãy kiểm tra lại !";
        toastr.error(error);
    }
}

function remove_sector_success_callback(response) {
    let result = response;
    if (result.success === true) {
        toastr.success(`Bạn đã xóa thành công nhóm ngành "${result.name}"`);
        get_all_sectors();
    }
    else {
        let error = '';
        if (result.code === "doesnotexist") {
            error = `Nhóm ngành này không tồn tại!`;
        }
        else error = "Không thể sửa nhóm ngành này. Bạn hãy kiểm tra lại !";
        toastr.error(error);
    }
}

function get_all_sectors() {
    let url = '/api/v1/sectors';
    ajax_request(false, true, "GET", "json", url, null, null, sectors_success_callback, error_callback)
}

function sectors_success_callback(response) {
    let sectors = response.sectors;
    let sector_length = response.sectors.length;
    let inner_sector = '';
    let inner_edit_sector = '';
    let inner_remove_sector = '';
    $.each(sectors, function (index, sector) {
        let name = capitalize(sector.name.toLowerCase());
        let reverse_name = capitalize(sectors[sector_length - index -1].name.toLowerCase());
        // console.log(sectors[sector_length - index - 1].name);
        inner_sector += `<div class="col-12 px-0 my-2 animated fadeIn"><i class="la la-angle-double-right"></i> ${reverse_name}</div>`;
        inner_edit_sector += `<option value="${sector.id}">${name}</option>`;
        inner_remove_sector += `<div class="col-12 my-3">
                                    <button type="button" class="btn btn-sm btn-warning m--pull-right sector-remove-btn" sector-name="${name}" sector-id="${sector.id}" data-toggle="modal"
                                        data-target="#confirm-modal">Xóa</button>
                                    <span value="${sector.id}" name="sector_id"> ${name}</span>;
                                    <hr>
                                </div>`;
    });
    $('#total-sector').html(`<h4>Hiện có ${sector_length} nhóm ngành</h4>`);
    $('#sectors-portlet').empty().html(inner_sector);
    $('#sector-edit-select-form').html(inner_edit_sector);
    $('#sector-remove-form').html(inner_remove_sector);
};

function error_callback(response) {
    alert("Có lỗi xảy ra, xem thêm tại console!")
}

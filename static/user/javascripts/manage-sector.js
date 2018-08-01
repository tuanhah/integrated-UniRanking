$(document).ready(function () {
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": true,
        "progressBar": false,
        "positionClass": "toast-top-right",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "200",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };
    get_all_sectors();
    $("#add-sector").submit(function (e) {
        e.preventDefault();
        let csrftoken = getCookie("csrftoken");
        let data = $(this).serializeArray();
        data.push({
            name: "csrfmiddlewaretoken",
            value: csrftoken
        });
        let url = "/api/v1/add_sector";
        ajax_request(false, true, "POST", "json", url, null, data, add_sector_success_callback, error_callback);
    });
});

function add_sector_success_callback(response) {
    let result = response['message'];
    if (response.success == true) {
        toastr.success(result);
        get_all_sectors();
    }
    else toastr.error(result);
}

function get_all_sectors() {
    let url = '/api/v1/sectors';
    ajax_request(false, true, "GET", "json", url, null, null, sectors_success_callback, error_callback)
}

function sectors_success_callback(response) {
    let sectors = response.sectors;
    let sector_length = response.sectors.length;
    let inner_sector = '';
    $.each(sectors, function (index, sector) {
        let name = capitalize(sector.name.toLowerCase());
        inner_sector += `<div class="col-12 px-0 my-2"><i class="la la-angle-double-right"></i> ${name}</div>`;
    });
    $('#total-sector').html(`<h4>Hiện có ${sector_length} nhóm ngành</h4>`)
    $('#sectors-portlet').html(inner_sector);
}


function error_callback(response) {
    alert("Có lỗi xảy ra, xem thêm tại console!")
}

function capitalize(text) {
    return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
}
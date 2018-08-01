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

    $("#add-sector").submit(function (e) {
        e.preventDefault();
        let csrftoken = getCookie("csrftoken");
        let data = $(this).serializeArray();
        data.push({
            name: "csrfmiddlewaretoken",
            value: csrftoken
        });
        let url = "/api/v1/add_sector";
        ajax_request(false, true, "POST", "json", url, null, data, add_sector_success_callback, print_error);
    });
});

function add_sector_success_callback(response) {
    let result = response['message'];
    if (response.success == true) {
        toastr.success(result);
    }
    else toastr.error(result);
}

function print_error(response) {
    alert("Có lỗi xảy ra, xem thêm tại console!")
}

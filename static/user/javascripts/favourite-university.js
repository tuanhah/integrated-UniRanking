var logined = $('#user-authenticated').attr('logined');
var current_user = $('#user-menu').attr('user-id');
$(document).ready(function () {
    let university_id = '';
    if (logined == 'true') {
        get_favourite_universities(current_user);
    };
    $(document).on('click', '.udelete-btn', function () {
        let modal_inner = '';
        let name = $(this).attr('university-name');
        modal_inner += `Bạn chuẩn bị xóa trường <strong>${name}</strong> ra khỏi danh sách yêu thích. Bạn có chắc chắn muốn xóa không?`;
        $('#confirm-delete-modal .modal-body').html(modal_inner);
        university_id = $(this).attr('university-id');
    });

    $(document).on('click', '#confirm-btn', function () {
        remove_favourite_university(current_user, university_id);
    });
});

function get_favourite_universities(user_id) {
    let url = `/api/v1/user/favourite?user=${user_id}`;
    ajax_request(false, true, "GET", "json", url, null, null, favourite_universities_success_callback, error_callback);
}

function favourite_universities_success_callback(response) {
    favourite_universities = response.favourite_universities;
    let inner = '';
    $.each(favourite_universities, function (index, f_univ) {
        inner += `<div class="col-lg-6 animated flipInY">
                    <div class="m-portlet m-portlet--bordered-semi m-portlet--full-height  m-portlet--rounded-force">
                        <div class="m-portlet__head m-portlet__head--fit">
                            <div class="m-portlet__head-caption">
                                <div class="m-portlet__head-action">
                                    <button type="button" class="btn btn-sm m-btn--pill  btn-brand">#${f_univ.general_statistics.rank}</button>
                                </div>    
                            </div>
                            <div class="m-portlet__head-tools">
                                <ul class="m-portlet__nav">
                                    <li class="m-portlet__nav-item">
                                        <button type="button" class="btn btn-sm m-btn--pill btn-danger udelete-btn" data-toggle="modal" data-target="#confirm-delete-modal" university-name="${f_univ.university.name}" university-id="${f_univ.university.id}">Xóa</button>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="m-portlet__body">
                            <div class="m-widget19">
                                <div class="m-widget19__pic m-portlet-fit--top m-portlet-fit--sides" style="min-height-: 286px">
                                    <img src="../../../static/share/images/vnu_cover.jpg" alt="">
                                    <h3 class="m-widget19__title m--font-light">
                                        
                                    </h3>
                                    <div class="m-widget19__shadow"></div>
                                </div>
                                <div class="m-widget19__content">
                                    <div class="m-widget19__header">
                                        <div class="m-widget19__user-img">
                                            <img class="m-widget19__img" src="../../../static/share/images/vnu_avatar.jpg" alt="">
                                        </div>
                                        <div class="m-widget19__info">
                                            <span class="m-widget19__username m--regular-font-size-lg2" style="line-height:160%" class="university-name" >${f_univ.university.name}
                                            </span>
                                            <br>
                                            <span class="m-widget19__time">
                                                ${f_univ.university.address}
                                            </span>
                                        </div>
                                        <div class="m-widget19__stats">
                                            <!--<span class="m-widget19__number m&#45;&#45;font-brand">-->
                                                <!--{f_univ.general_statistics.avg_score}-->
                                            <!--</span>-->
                                            <!--<span class="m-widget19__comment">-->
                                                <!--#-->
                                            <!--</span>-->
                                        </div>
                                    </div>
                                    <div class="m-widget19__body">
                                        ${f_univ.university.overview}
                                    </div>
                                </div>
                                <div class="m-widget19__action">
                                    <a href="${f_univ.university.site_href}" target="_blank" class="btn m-btn--pill btn-secondary m-btn m-btn--hover-brand m-btn--custom">Xem thông tin ...
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`;
    });
    $('#favourite-university-area').html(inner);
}

function remove_favourite_university(user, university) {
    let csrftoken = getCookie("csrftoken");
    let url = '/api/v1/edit/favourite/remove_university';
    data = [{
        name: "university",
        value: university
    }];
    data.push({
        name: "csrfmiddlewaretoken",
        value: csrftoken
    });
    ajax_request(false, true, "POST", "json", url, null, data, remove_favourite_universities_success_callback, error_callback);
}

function remove_favourite_universities_success_callback(response) {
    let result = response;
    if (result.success === true) {
        toastr.info(`Bạn đã xoá thành công trường "${result.name}" khỏi danh sách yêu thích`);
    }
    else {
        let error = '';
        error = "Không thể xóa trường này. Bạn hãy kiểm tra lại !";
        toastr.error(error);
    }
    let current_user = $('#user-menu').attr('user-id');

    get_favourite_universities(current_user);

}

function error_callback(response) {
    alert("Đã xảy ra lỗi, xem response tại console !!")
}


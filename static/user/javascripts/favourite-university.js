var logined = $('#user-authenticated').attr('logined');
var current_user = $('#user-menu').attr('user-id');
$(document).ready(function () {
    if(logined == 'true') {
        get_favourite_universities(current_user);
    }
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
                                            <span class="m-widget19__username m--regular-font-size-lg2" style="line-height:160%">
                                                ${f_univ.university.name}
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
    $('#favourite-university-area').html(inner)
}

function error_callback(response) {
    alert("Đã xảy ra lỗi, xem response tại console !!")
}


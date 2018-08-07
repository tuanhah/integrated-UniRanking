var logined = $('#user-authenticated').attr('logined');
var current_user = $('#user-menu').attr('user-id');
var BootstrapSelect={init:function(){$(".m_selectpicker").selectpicker()}};jQuery(document).ready(function(){BootstrapSelect.init()});
$(document).ready(function () {
	if(logined == 'true') {
		get_manage_universities(current_user);
    }

});

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
                            <span><button href="#" class="m-btn m-btn--pill m-btn--hover-info btn btn-sm btn-secondary mx-2" university-id="${university.id}" data-toggle="modal" data-target="#sector-modal">Quản lý ngành</button></span>                        	
                            <span><button href="#" class="m-btn m-btn--pill m-btn--hover-accent btn btn-sm btn-secondary" university-id="${university.id}" data-toggle="modal" data-target="#score-modal">Quản lý điểm</button></span>
						</div>
                    </div>`;
		// $('.m-widget4').append(inner);
	});
	$('.m-widget4').empty().html(inner);
}

function error_callback(response) {
	alert("Đã xảy ra lỗi, xem response tại console !!")
}
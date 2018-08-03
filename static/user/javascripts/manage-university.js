var logined = $('#user-authenticated').attr('logined');
var current_user = $('#user-menu').attr('user-id');
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
	console.log(response);
}

function error_callback(response) {
	alert("Đã xảy ra lỗi, xem response tại console !!")
}
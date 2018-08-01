var current_user = $('#user-menu').attr('user-id');
$(document).ready(function () {
	get_favourite_universities(current_user);
});

function get_favourite_universities(user_id) {
	let url = `/api/v1/user/favourite?user=${user_id}`;
	ajax_request(false, true, "GET", "json", url, null, null, favourite_universities_success_callback, error_callback);
}

function favourite_universities_success_callback(response) {
	console.log(response);
}

function error_callback(response) {
	alert("Đã xảy ra lỗi, xem response tại console !!")
}
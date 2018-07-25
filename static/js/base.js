window.onbeforeunload = function() {
	// window.scrollTo(0,0);
	jQuery("html, body").animate({
			scrollTop: jQuery("body").offset().top
			// document.documentElement.scrollTop = 0,
	}, 120);
}
$(document).ready(function () {
	
	$(window).resize(function(){
		var img_width = $('.background-img').parent().width();
		$('.background-img').css({'width':img_width});
	});
	window.onscroll = function () {
		scroll();
	};
	function scroll() {
		if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
			$("#gotop").css({display: "block"});
		}
		else $("#gotop").css({display: "none"});
	};

	jQuery("#gotop").click(function () {
		jQuery("html, body").animate({
			scrollTop: jQuery("body").offset().top
			// document.documentElement.scrollTop = 0,
		}, 250);
	});

	$("#login_form").submit(function (e) {
		e.preventDefault();
		let csrftoken = getCookie("csrftoken");
		let data = $(this).serializeArray();
		data.push({
			name: "csrfmiddlewaretoken",
			value: csrftoken
		});
		let url = "/api/v1/auth";
		ajax_request(false, true, "POST", "json", url, null, data, login_success_reload, print_response);
	});

	$("#signup_form").submit(function (e) {
		e.preventDefault();
		let csrftoken = getCookie("csrftoken");
		let data = $(this).serializeArray();
		data.push({
			name: "csrfmiddlewaretoken",
			value: csrftoken
		});
		let url = "/api/v1/register";
		ajax_request(false, true, "POST", "json", url, null, data, register_success, print_response);
	});

	$(".modal").on("hidden.bs.modal", function () {
		// $(this).find("input").val("");
		$(".alert").empty();
		$("#signup_errors").addClass('d-none');
		
	});
	
});

function scroll_to_id($this) {
	jQuery($this.attr("show")).show();
	jQuery("html, body").animate({
		scrollTop: jQuery($this.attr("show")).offset().top - 110
	}, 400);
}


function ajax_request(cache_, async_, type_, data_type_, url_, headers_, data_, success_, error_) {
	return $.ajax({
		cache: cache_,
		async: async_,
		type: type_,
		dataType: data_type_,
		headers: headers_,
		url: url_,
		data: data_,
		success: function (response) {
			success_ != null && success_(response);
		},
		error: function (response) {
			error_ != null && error_(response);
		}
	});
}

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		var cookies = document.cookie.split(";");
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			if (cookie.substring(0, name.length + 1) === name + "=") {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

function print_response(response) {
	console.log(response);
}

function login_success_reload(response) {
	let login_error_dom = $("#login_errors").hide();
	if (response.success == true) {
		window.location.reload();
	} else {
		list_error = message_to_html(response);
		login_error_dom.append(list_error);
		$('#login_errors').removeClass('d-none');
		
	}
}

function register_success(response) {
	let error_dom = $("#signup_errors"),
		success_dom = $("#signup_success");
	error_dom.empty();
	success_dom.empty();	
	if (response.success == true) {
		success_dom.text("Đăng ký thành công !");
		error_dom.addClass('d-none');
		success_dom.removeClass('d-none');
		window.location.reload();
		
	} else {
		let list_error = message_to_html(response);
		error_dom.append(list_error);
		error_dom.removeClass('d-none');
	}
}

function message_to_html(message) {
	let list_error = "";
	$.each(message, function (field, errors) {
		list_error += field + " :<ul>";
		$.each(errors, function (code, error) {
			list_error += "<li>" + error.message + "</li>";
		});
		list_error += "</ul>";
	});
	return list_error;
}

document.onreadystatechange = function () {
  	var state = document.readyState
  	if (state == 'complete') {
        $('.dom-loader').fadeOut(500);
  	}
};
// $('#navibar').addClass('navbar__over');
$(document).ready(function(){
	$('#navibar').addClass('navbar__over');
	get_universities_list();
	jQuery('#uni-info-btn').click(function() {
	    var uniName = jQuery('.info-multiple-select').find('option:selected').attr('u-name');
	    jQuery('#uni-name').text(uniName);
	    $('#all-info').show();
	});
	
	$(document).on("change", "#university-select-list", function(){
		selected_univ = [];
		let univ_box = '';
		$("#university-select-list option:selected").each(function(){
			let univ_id = $(this).val();
			let url = `/university/${univ_id}`;
			page_redirect(url);
		});
	});
	$(document).on("click touch", ".info--remove-univ", function(){
		let id = $(this).attr('university-id');
		let name = $(this).attr('university-name');
		let values = $('#university-select-list').val();
		if(values){
			let i = values.indexOf(id);
			if(i >= 0){
				values.splice(i, 1);
				$('#university-select-list').val(values).change();
			}
		}
		// iziToast.destroy();
		// iziToast.warning({
		// 	title: `Đã xóa ${name} khỏi danh sách so sánh!`,
		// 	position: 'bottomLeft',
		// });
		$("#selected-univ").html('<strong>Ban chua chon truong nao!</strong>');
		$('#university-select-list').trigger("chosen:updated");
	});
});
function page_redirect(url) {
	window.location.href = url;
};

function error_callback(response) {
    console.log(response)
    alert("Có lỗi trong quá trình lấy dữ liệu.")
};

function get_universities_list(){
	let url = '/api/v1/universities';
	let data = {
	};
	ajax_request(false, true, "GET", "json", url, data, null, all_universities_success_callback, error_callback);
};

function all_universities_success_callback(response){
        let universities = response.universities;
        let pane = ''
        $.each(universities, function(index, university){
            pane += `<option value="${university.id}" univ-name="${university.name}" >${university.name}</option>`
        });
	    $("#university-select-list").html(pane);
        $("#university-select-list").chosen({max_selected_options: 1});

};


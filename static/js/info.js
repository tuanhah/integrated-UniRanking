document.onreadystatechange = function () {
  var state = document.readyState
  if (state == 'complete') {
         // document.getElementById('interactive');
         // document.getElementById('load').style.visibility="hidden";
         alert("ready");
  }
};
jQuery(document).ready(function(){
	// $('.loader-img').fadeIn(200).delay(500).animate({height:"hide"},300);
	get_universities_list();
	jQuery('#uni-info-btn').click(function() {
	    var uniName = jQuery('.info-multiple-select').find('option:selected').attr('u-name');
	    jQuery('#uni-name').text(uniName);
	    $('#all-info').show();
	});

	$(document).on("change", "#university-select-list", function(){
		selected_univ = [];
		//let li_count = $("#comp_subj_multiselect_chosen .chosen-choices").find("li").length;
		//let last_select_univ = $('#comp_subj_multiselect_chosen .chosen-choices').find('li').eq(li_count - 2).find('span').text();
		let univ_box = '';

		$("#university-select-list option:selected").each(function(){
			let univ_name = $(this).attr('univ-name');
			let univ_id = $(this).val();
			let data = {
				id : univ_id,
				name : univ_name,
			};
			selected_univ.push(data);
			$('#univ-info-btn').attr('href',`/university/${univ_id}`);
		});
		// iziToast.success({
		// 	title: `Đã thêm ${last_select_univ} vào danh sách so sánh!`,
		// 	position: 'bottomLeft',
		// });
		$.each(selected_univ, function(index, university){
			univ_box += ` <strong>Da chon: </strong><i title="Xóa khỏi danh sách" data-toggle="tooltip" class="fa fa-remove info--remove-univ right-icon ml-3 mt-1" university-id="${university.id}" university-name="${university.name}"></i> ${university.name}`;
		});
		$("#selected-univ").html(univ_box);
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


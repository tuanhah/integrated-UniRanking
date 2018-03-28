jQuery(document).ready(function() 		{
	jQuery('#ranking-table').DataTable();
	jQuery('#r-by-s-btn').click(function() {
		jQuery('#r-table-area-u').hide();
	});
	jQuery('#r-by-u-btn').click(function(){ 
		$('#r-select-subject, #r-table-area-s').hide();
	});
});
var subject_json;
jQuery(document).on('click', '.subject-btn', function(){
	jQuery('.subject-btn').removeClass('btn-select');
	jQuery(this).addClass('btn-select');
	$('.subject-btn').find($('.fa')).removeClass('fa-check');
	$(this).find($('.fa')).addClass('fa-check');
	var subject_id = $(this).attr('id-subject');
	let subject = $(subject_json).filter(function(i, n){
		if(n.id == subject_id) return n;
	});
	$('#r-s-table-title').html('Bảng xếp hạng ngành ' + subject[0].name);
});
$(document).on('click', '.gs1-btn', function(){
	$('.gs1-btn').removeClass('btn-select');
	$(this).addClass('btn-select');
	var sector_id = $(this).attr('id-gs1');
	$('#r-subject-area').html('<div class="alert alert-warning mx-auto mt-3">Bạn chưa chọn nhóm ngành</div>');
	update_sector_choice(sector_id);
	$('gs1-btn').find($('.fa')).removeClass('fa-check');
	$(this).find($('.fa')).addClass('fa-check');
});
$(document).on('click', '.gs2-btn', function(){
	$('.gs2-btn').removeClass('btn-select');
	$(this).addClass('btn-select');
	$('.gs2-btn').find($('.fa')).removeClass('fa-check');
	$(this).find($('.fa')).addClass('fa-check');
	var group_id = $(this).attr('id-gs2');
	update_group_choice(group_id);

});
get_all_sectors();
function error_callback(response){
	alert("Đã xảy ra lỗi!");
	console.log(response);
}
function get_all_sectors(){
	let csrftoken = getCookie('csrftoken');
	let url = "/api/sectors";
	let data = {
		csrfmiddlewaretoken: csrftoken,
	};
	ajax_request(data, "POST", "json", url, all_sectors_success_callback, error_callback);
}
function all_sectors_success_callback(response){
	if(response.success){
		let sectors = response.sectors;
		let pane = "";
		$.each(sectors, function(index, sector){
			pane += `<div class="col-md-4"><a class="btn gs-btn gs1-btn" href="#r-select-subject" id-gs1="${sector.id}">${sector.name}<i class="fa mt-1" style="float:right"></i></a></div>`;
		});
		$('#r-gs1-area').html(pane);
	}
}
function update_sector_choice(sector_id){
	let csrftoken = getCookie('csrftoken');
	let url = "/api/groups";
	let data = {
		csrfmiddlewaretoken: csrftoken,
		sector: sector_id,
	};
	ajax_request(data, "POST", "json", url, groups_success_callback, error_callback);
}
function groups_success_callback(response){
	if(response.success){
		let groups = response.groups;
		let pane = "";
		$.each(groups, function(index, group){
			pane += `<div class="col-md-4"><a class="btn gs-btn gs2-btn" href="#r-select-subject" id="r-gs-2-${group.id}" id-gs2="${group.id}">${group.name}<i class="fa mt-1" style="float:right"></i></a></div>`;
		});
		$('#r-gs2-area').html(pane);
		$('#r-tab1, #r-groupSubject-1').removeClass('active');
		$('#r-tab2').addClass('active');
		$('#r-groupSubject-2').removeClass('fade').addClass('active');
	}
}
function update_group_choice(group_id){
	let csrftoken = getCookie('csrftoken');
	let url = "/api/allSubjects";
	let data = {
		csrfmiddlewaretoken: csrftoken,
		group: group_id,
	};
	ajax_request(data, "POST", 'json', url, subjects_success_callback, error_callback);
}
function subjects_success_callback(response){
	if(response.success){
		let subjects = response.subjects;
		let pane = "";
		$.each(subjects, function(index, subject){
			pane +=  `<div class="col-md-4"><a class="btn gs-btn subject-btn go-to-id" show="#r-table-area-s" href="#r-table-area-s" id="r-subject-${subject.id}" id-subject="${subject.id}">${subject.name}<i class="fa mt-1" style="float:right"></i></a></div> `
		});
		$("#r-subject-area").html(pane);
		$('#r-tab2, #r-groupSubject-2').removeClass('active');
		$('#r-tab3').addClass('active');
		$('#r-subject').removeClass('fade').addClass('active');
		subject_json = subjects;
	}
}
function get_category_criterion(target){
	let csrftoken = getCookie('csrftoken');
	let url = "/api/editor/categories";
	let data = {
		csrfmiddlewaretoken: csrftoken,
		target: target,
	}
	ajax_request(data, "POST", "json", url, category_criterion_success_callback, error_callback);
}
function category_crriterion_success_callback(response){
	if(response.success){
		let categories = response.categories;
		let pane = "";

	}
}
function get_criterion_of_id(category_id){
	let csrftoken = getCookie('csrftoken');
	let url = '/api/criterions';
	let data = {
		csrfmiddlewaretoken: csrftoken,
		id: category_id,
	};
	ajax_request(data, "POST", "json", url, criterion_success_callback, error_callback);
}
function criterion_success_callback(response){
	if(response.success){
		let criterions = response.criterions;
		let pane = "";
	}
}

jQuery(document).ready(function(){         
	jQuery('#subject-ranking').click(function(){
		jQuery('#ranking__subject_subj-selection, #step-2').hide().animate({opacity:'show'}, 500);
		jQuery('#ranking__university_univ-selection, #ranking__university-table, #ranking__university-table').hide();
		get_all_sector();
        get_all_category('subject');
	});
	var univ_th_ctgr;
	var univ_th_crtr;
	var univ_th_sort;
    var subj_table_body = '';
    var univ_table_body = '';
            
	jQuery('#university-ranking').click(function(){
        univ_th_ctgr = '';
        univ_th_crtr = '';
        univ_th_sort = '';
        // let universities = [];
        jQuery('#ranking__subject_subj-selection, #ranking__subject_univ-selection, #ranking__subject-table, #ranking__university-table').hide();
		jQuery('#ranking__university_univ-selection, #step-2').hide().animate({opacity:'show'}, 500);
        let url = '/api/v1/universities';
        let data = {

        };
        //ajax_request(false, true, "GET", "json", url, data, null, all_universities_success_callback, error_callback);
		get_all_category('university');
		


		
		$('.loader-img').fadeIn(200).delay(800).animate({height:"hide"},300);
		setTimeout(function(){
			set_table_title();
		},300);
		function set_table_title(){
    		var containerWidth = $('.rank_table').width();
            var num_of_ctgr = 5;
		    let univ_width = 350;
    		let rank_width = 63;
	    	let number_of_crtr = 3;
            univ_th_ctgr =`<th rowspan="2" class="subj-rank-th" style="width:${rank_width}px">Thứ hạng</th><th class='rank__univ_table-category-h' rowspan="2" style='width:${univ_width}px'>Trường</th>`;
            var ctgr_width = (containerWidth-rank_width-univ_width)/num_of_ctgr;
	    	univ_th_sort = '<th></th><th></th>';
		    $.each(univ_ctgrCrtr, function(ctgr_index, ctgr){
			    let colspan = Object.keys(ctgr.criteria).length;
			    let category = ctgr.criterion_category;
			    univ_th_ctgr += `<th class="comp__univ_table-category comp__univ_table-ctgr-${category.id}" colspan="${number_of_crtr}">${category.name}</th> `;
			    let crtrs = ctgr.criteria;
			    $.each(crtrs, function(crtr_index, crtr){
				    if(crtr_index <= number_of_crtr - 1){
					    univ_th_crtr += `<th class="comp__univ_table-criterion comp__univ_table-${category.id}-cr" criterion-id="${crtr.id}">${crtr.name}</th>`;
					    univ_th_sort += '<th> </th>';
				    }
		    	});
            });
            
		}	


	    setTimeout(function() {   
			$('#university_table_th-ctgr').html(univ_th_ctgr);
			$('#university_table_th-crtr').html(univ_th_crtr);
			$('#university_table_th-sort').html(univ_th_sort);
        }, 400);

		$($(this).attr('show')).animate({opacity:"show"},1000);
        $('html, body').animate({scrollTop:$($(this).attr('show')).offset().top - 104}, 1000);
    });
    
    var subj_table_th ="";
    var subj_ctgrCrtr = [];
    var ctgr_with_criterions = [];
    var scores = [];
    var score_list = new Array();
    var crtr_width =171;
    function translate(){
    	jQuery('#DataTables_Table_0_length label').contents().first()[0].textContent="Số trường trên bảng: ";
    	jQuery('#DataTables_Table_0_length label').contents().last()[0].textContent=" trường."
    	jQuery('#DataTables_Table_0_filter label').contents().first()[0].textContent="Tìm kiếm: ";
    	jQuery('a[data-dt-idx="0"]').text("Trang trước");
    	jQuery('a[data-dt-idx="8"]').text("Trang sau");
    	let Info = jQuery("#DataTables_Table_0_info");
    	Info.html(Info.html().replace("Showing", "Đang thể hiện trên bảng từ trường số "));
    	Info.html(Info.html().replace("to", " tới trường số "));
    	Info.html(Info.html().replace("of", " trên tổng số "));
    	Info.html(Info.html().replace("entries", " trường."));
        // alert($('#rank-subj-multiselect option:selected').length);
    }
    
    var groups_list;
    var univ_table_th = ""; var univ_ctgrCrtr = [];
    jQuery(document).on('click', '.gs1-btn', function(){
    	jQuery('#ranking__subject_univ-selection').hide();
    	jQuery('.gs1-btn').removeClass('btn-select');
    	$('.gs1-btn').find($('.fa')).removeClass('fa-check');
    	jQuery(this).addClass('btn-select');
    	$(this).find($('.fa')).addClass('fa-check');
    	let sector_id = $(this).attr('id-gs1');
    	$('#subject-area').html('<div class="alert alert-warning mx-auto mt-3">Bạn chưa chọn nhóm ngành</div>');
    	// update_sector_choice(sector_id);
        let url = `/api/v1/sectors/${sector_id}/subjects`;
        ajax_request(false, true, "GET", "json", url, null, null, group_success_callback, error_callback);
    });
    jQuery(document).on('click', '.gs2-btn', function(){
    	jQuery('#ranking__subject_univ-selection').hide();
    	jQuery('.gs2-btn').removeClass("btn-select");
    	$('.gs2-btn').find($('.fa')).removeClass('fa-check');
    	jQuery(this).addClass('btn-select');
    	$(this).find($('.fa')).addClass('fa-check');
    	let group_id = $(this).attr('id-gs2');
    	// update_group_choice(group_id);
        let subject_list = jQuery(groups_list).filter(function(index, entry){
            if(entry.group.id == group_id) return entry;
        });
        subjects_list_of_group(subject_list[0].subjects);
    });
    jQuery(document).on('click', '.subject-btn', function(){
		
    	jQuery('.subject-btn').removeClass('btn-select');
    	jQuery(this).addClass('btn-select');
    	$('.subject-btn').find($('.fa')).removeClass('fa-check');
    	$(this).find($('.fa')).addClass('fa-check');
    	let subjectName = $(this).attr('subject-name');
        $('#c-s-tit-31').text('Chọn trường ngành ' + subjectName);
        $('#ranking__subject_table-title').text('So sánh ngành ' + subjectName);
        let subject_selected_id = parseInt($(this).attr('subject-id'));
        let url = '/api/v1/universities';
        let data = {
            // subject : subject_selected_id,
            // subject : 1,
        };
		var subj_th_ctgr = '';
		var subj_th_crtr = '';
        var subj_th_sort = '';
        subj_table_body = '';
        ajax_request(false, true, "GET", "json", url, null, data, universities_success_callback , error_callback);
	
		
        // function translate(){
		//     jQuery('#DataTables_Table_0_length label').contents().first()[0].textContent="Số trường trên bảng: ";
        // 	jQuery('#DataTables_Table_0_length label').contents().last()[0].textContent=" trường."
        // 	jQuery('#DataTables_Table_0_filter label').contents().first()[0].textContent="Tìm kiếm: ";
    	//     jQuery('a[data-dt-idx="0"]').text("Trang trước");
        // 	jQuery('a[data-dt-idx="8"]').text("Trang sau");
        // 	let Info = jQuery("#DataTables_Table_0_info");
    	//     Info.html(Info.html().replace("Showing", "Đang thể hiện trên bảng từ trường số "));
        // 	Info.html(Info.html().replace("to", " tới trường số "));
        // 	Info.html(Info.html().replace("of", " trên tổng số "));
    	//     Info.html(Info.html().replace("entries", " trường."));
        // // alert($('#rank-subj-multiselect option:selected').length);
        // }

        $('.loader-img').fadeIn(200).delay(800).animate({height:"hide"},300);
        var containerWidth = $('.rank_table').width();
		var num_of_ctgr = 4;
		var num_of_crtr = 4;//$('#rank-subj-multiselect :selected').length;
		let univ_width = 350;
		let rank_width = 63;
        subj_th_ctgr =`<th rowspan="2" style="width:${rank_width}px">Thứ hạng</th><th class='rank__subj_table-category-h' rowspan="2" style='width:${univ_width}px'>Trường</th>`;
        var ctgr_width = (containerWidth-univ_width)/num_of_ctgr;
		subj_th_sort = '<th></th><th></th>';
		$.each(subj_ctgrCrtr, function(ctgr_index, ctgr){
			let colspan = Object.keys(ctgr.criteria).length;
			let category = ctgr.criterion_category;
			subj_th_ctgr += `<th class="comp__subj_table-category comp__subj_table-ctgr-${category.id}" colspan="${num_of_crtr}">${category.name}</th> `;
			let crtrs = ctgr.criteria;
			$.each(crtrs, function(crtr_index, crtr){
				if(crtr_index <= num_of_crtr - 1){
					subj_th_crtr += `<th class="comp__subj_table-criterion comp__subj_table-${category.id}-cr" crtr-id="${crtr.id}" ctgr-id="${category.id}">${crtr.name}</th>`;
					subj_th_sort += '<th> </th>'
				}
			});
		});

        setTimeout(function() {   
			$('#subject_table_th-ctgr').html(subj_th_ctgr);
			$('#subject_table_th-crtr').html(subj_th_crtr);
			$('#subject_table_th-sort').html(subj_th_sort);
            translate();
        }, 300);

		$($(this).attr('show')).animate({opacity:"show"},1000);
        $('html, body').animate({scrollTop:$($(this).attr('show')).offset().top - 104}, 1000);
        
	});
    function error_callback(response){
    	alert("Đã xảy ra lỗi, xem response tại console");
    }
    
    function group_success_callback(response){
    	
        let groups = response; groups_list = groups;
        let pane = "";
        $.each(groups, function(index, group){
           pane += `<div class="col-md-4"><a href="#" show="#ranking__subject_subj-selection" class="btn gs-btn gs2-btn go-to-id" id="gs-2-${group.group.id}" id-gs2="${group.group.id}">${group.group.name}<i class="fa mt-1" style="float:right"></i></a></div>`; 
       });
        $('#gs2-area').html(pane);
        $('#tab1, #groupSubject-1').removeClass('active');
        $('#tab2').addClass('active');
        $('#groupSubject-2').removeClass('fade');
        $('#groupSubject-2').addClass('active');

    }

    function subjects_list_of_group(subjects){
    	let pane = "";
        $.each(subjects, function(index, subject){
            pane += `<div class="col-md-4"><a show="#ranking__subject-table" href="#" class="btn gs-btn subject-btn go-to-id" id="subject-${subject.id}" subject-name="${subject.subject}" subject-id="${subject.id}">${subject.subject}<i class="fa mt-1" style="float:right"></i></a></div>`;
        });
        $('#subject-area').html(pane);
        $('#tab2, #groupSubject-2').removeClass('active');
        $('#tab3').addClass('active');
        $('#subject').removeClass('fade');
        $('#subject').addClass('active');
    };
    var univ_for_test = [];
    function universities_success_callback(response){
        let universities = response;
        score_list = [];
        $.each(universities, function(index, university){
            if(university.id == 1 || university.id == 24 || university.id == 135 || university.id == 174 || university.id == 175 || university.id == 13){
                // subj_table_body += `<tr><td>1</td><td>${university.name}</td>`;
                univ_for_test[`${university.id}`] = university;
                scores_list_for_subject_ranking(parseInt(university.id));
            }
            
        });
        setTimeout(function(){
            univ_for_test.forEach(function(univ, index) {
                
                let univ_id = univ.id;
                subj_table_body += `<tr><td class="subj-rank">1</td><td class="subj__table_univ-name">${univ.name}</td>`;
                for (let i = 0; i < 16; i++) {
                    let crtr_id = $(`#subject_table_th-crtr th:nth-child(${i+1})`).attr('crtr-id');
                    let ctgr_id = parseInt($(`#subject_table_th-crtr th:nth-child(${i+1})`).attr('ctgr-id'));
                    let ctgr_index = parseInt(i/4);

                    if(score_list[univ_id] != undefined){
                        if(score_list[univ_id].length != 0){                            
                            $(score_list[univ_id][ctgr_index + 1].criterion_scores).filter(function(i, entry){
                                if(entry.criterion.id == crtr_id){
                                    detail = entry.score;
                                }
                            });
                        }
                        else detail = "E!";
                    }
                    else detail = "E!";
                    subj_table_body += `<td class="comp__subj_table-${univ_id} comp__subj_table-cr-${crtr_id} comp__subj_score-ctgr-${ctgr_id}">${detail}</td>`;
                    
                }
                subj_table_body += '</tr>'; 
            });
            
        }, 300);
        setTimeout(function(){
            $('#ranking__university_table-tbody').html(subj_table_body);
            // setWidth();
            $('.sortable').DataTable();
            
        }, 350);
        setTimeout(function(){
            jQuery('#subject_table_th-crtr th').each(function(){
                let id = $(this).attr('crtr-id');
                let width = ($(this).width()+1);
                $(`.comp__subj_table-cr-${id}`).width(width);
            });

            // $('.subj-rank').width($('.subj-rank-th').width());
            $('.subj__table_univ-name').width($('.rank__subj_table-category-h').width() + 17);
        
        },400)
    };

    function all_universities_success_callback(response){
        let universities = response;
        $.each(universities, function(index, university){
            univ_table_body += `<tr><td>1</td><td>${university.name}</td>`;
            scores_list_for_university_ranking(parseInt(university.id));
        });
        
        
    };
    var selected_univ = [];
    
    
    function get_all_sector(){
        let url = "/api/v1/sectors";
        ajax_request(false, true, "GET", "json", url, null, null, all_sectors_success_callback, error_callback);
    };
    function all_sectors_success_callback(response){
        let sectors = response;
        let pane = "";
        $.each(sectors, function(index, sector){
            pane += `<div class="col-md-4"><a show="#ranking__subject_subj-selection" class="btn gs-btn gs1-btn go-to-id" href="#" id-gs1="${sector.id}">${sector.name}<i class="fa mt-1" style="float:right"></i></a></div>`;
        });
        $("#gs1-area").html(pane);

    }

    function get_all_category(target){
        let url = "/api/v1/criteria";
        let data = {
            target : target,
        };
        if(target == "subject"){
            ajax_request(false, true, "GET", "json", url, null, data, all_category_subject_callback, error_callback);
        }
        else if(target == "university"){
            // data={};
            ajax_request(false, true, "GET", "json", url, null, null, all_category_university_callback, error_callback);
        }
    }
    function all_category_subject_callback(response){
        let categories = response;
        subj_ctgrCrtr = categories;
        
    }
    function all_category_university_callback(response){
        univ_ctgrCrtr = response;
    }
    
    function scores_list_for_subject_ranking(university_id){
        let uni_id = university_id;
        let url = `/api/v1/universities/${uni_id}/scores`;
        let data = {
            university_id : university_id,
        };
        ajax_request(false, true, "GET", "json", url, null, data, score_list_subject_ranking_success_callback, error_callback);
    }
	var scores_index = 0;
	function score_list_subject_ranking_success_callback(response){
        response_id = response.university_id;
        score_list[`${response_id}`] = response.score;
	}

	function scores_list_for_university_ranking(university_id){
        let uni_id = university_id;
        let url = `/api/v1/universities/${uni_id}/scores`;
        let data = {
            university_id : university_id,
        };
        ajax_request(false, true, "GET", "json", url, null, data, score_list_university_ranking_success_callback, error_callback);
    }
    // var scores_index = 0;
    function score_list_university_ranking_success_callback(response){
        response_id = response.university_id;
        score_list[`${response_id}`] = response.score;
        
	}

});
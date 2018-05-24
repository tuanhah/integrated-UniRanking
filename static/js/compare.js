$(document).ready(function(){

    var subj_table_th ="";
    var subj_ctgrCrtr = [];
    var scores = [];
    var score_list = new Array();
    var ctgr_width = 161;
    var crtr_width = 250;
    var subjectId;
    var groups_list;
    var univ_table_th = ""; var univ_ctgrCrtr = [];
    var subj_display = true;
    var univ_display = true;
    var blank_selection = '<div class="blank-select my-1 text-center"></div>';
    var selected_univ = [];
    var scores_index = 0;
    var scard = $('.selection-card');
    var fcard = $('.fixed-card');
    var scard_pos = scard.position();
    var select_area = $('.select-area');

    iziToast.settings({
        timeout:2500,
    });

    $(window).scroll(function () {
        if($('#compare__university-table').css('display') == "none" && $('#compare__subject-table').css('display') == "none" && $(window).width() >= 992) {
	        var window_pos = $(window).scrollTop();
	        var select_area_height = select_area.height();

	        if (window_pos + 60 >= scard_pos.top && window_pos + 60 + fcard.height() <= select_area.position().top + select_area_height) {
		        $('.fixed-card').addClass('fixed--after-menu');
	        }
	        else {
		        $('.fixed-card').removeClass('fixed--after-menu');
	        }
        }
    });


	$(document).on('click touch','#subject-compare', function(){
        // iziToast.info({
        //     title: 'Đã chọn so sánh theo ngành',
        //     position: 'bottomLeft',
        // });
        let $this = $(this);
        $('#subject-compare i').remove();
        $('#subject-compare, #university-compare').removeClass('text-left');
        $(this).addClass('text-left').prepend(' <i class="fa fa-check-circle md-icon float-right"></i>');
        $('#university-compare i').remove();
        $('#compare__subject_subj-selection, #step-2').hide().animate({opacity:'show'}, 200, function(){;
            scroll_to_id($this);
        });
		$('#carousel-comp-area, #compare__university_univ-selection, #compare__university-table, #compare__university-table, #compare__subject-table, #compare__subject_univ-selection').hide();
        get_all_sector();
        get_all_category('subject');
        
    });

	$(document).on('click touch', '#university-compare', function(){
        // iziToast.info({
        //     title: 'Đã chọn so sánh theo trường',
        //     position: 'bottomLeft',
        // });
        let $this = $(this);
        $('#university-compare i').remove();
        $('#subject-compare, #university-compare').removeClass('text-left');
        $(this).addClass('text-left').prepend(' <i class="fa fa-check-circle md-icon float-right"></i>');
        $('#subject-compare i').remove();
        $('#carousel-comp-area, #compare__subject_subj-selection, #compare__subject_univ-selection, #compare__subject-table, #compare__university-table').hide();
		$('#compare__university_univ-selection, #step-2').hide().animate({opacity:'show'}, 200, function(){
            scroll_to_id($this);
        });

        //request for all universities list
		let url = '/api/v1/universities';
        let data = {
        };
        ajax_request(false, true, "GET", "json", url, data, null, all_universities_success_callback, error_callback);

        get_all_category('university');
    });
    
    $(document).on('click touch', '#compare__subject-btn', function(){
        if($('#comp-subj-multiselect option:selected').length > 1){
            $('.loader-img').fadeIn(200).delay(800).animate({height:"hide"},300);
            var containerWidth = $(window).width() * 0.94;
            var selectedNum = $('#comp-subj-multiselect :selected').length;
            crtr_width = 320;
            subj_table_th =`<th class='comp__subj_table-criterion-h' style='width:${crtr_width}px'>Tiêu chí</th>`;
            var table_tbody = "";
            scores = []; scores_index = 0; score_list = [];
            univ_width = (containerWidth-crtr_width)/selectedNum;

            $('#comp-subj-multiselect option:selected').each(function(index){
                let tmp = $(this).text();
                let id = $(this).val();
                subj_table_th += `<th class="subject-univ-${id}" style="width:${univ_width}px">` + tmp + '</th>';
                scores_list_for_subject_compare(parseInt(id), parseInt(subjectId));
            });
            $('#compare__subject_table-th').html(subj_table_th);
            $($(this).attr('show')).animate({opacity:"show"},1000);
            $('html, body').animate({scrollTop:$($(this).attr('show')).offset().top - 104}, 1000);
        }
        else{
            $('html, body').animate({scrollTop:$('#compare__subject_univ-selection').offset().top - 70}, 200);
            iziToast.error({
                title: 'Bạn phải chọn ít nhất 2 trường để so sánh!',
                position: 'bottomLeft',
            });
            $($(this).attr('show')).hide();
        }
    });

    // $('#subj-back-btn, #univ-next-btn').hover(function(){
    //     $(this).animate({
    //         width: "27%",
    //     }, "slow");
    // }, function(){
    //     $(this).animate({
    //         width: "25%",
    //     }, "slow");
    // });

    $(document).on('click', '#subj-back-btn', function(){
        let $this = $(this);
        $('#compare__subject_subj-selection').hide().animate({opacity:'show'}, 200, function(){;
            scroll_to_id($this);
        });
		$('#compare__university_univ-selection, #compare__subject_univ-selection').hide();
    });

    $(document).on('click', '#univ-next-btn', function(){
        let $this = $(this);
        $('#compare__subject_subj-selection').hide();
        $('#compare__subject_univ-selection').hide().animate({opacity:"show"},200, function(){
            scroll_to_id($this);
        });
    });

    $(document).on('click touch', '#compare__university-btn', function(){
        if($('#comp-univ-multiselect option:selected').length > 1){
            $('.loader-img').fadeIn(200).delay(800).animate({height: "hide"}, 300);
            var containerWidth = $('.comp_table').width();
            var selectedNum = $('#comp-univ-multiselect :selected').length;
            ctgr_width = 161;crtr_width = 320;
            univ_table_th =`<th class='comp__univ_table-criterion-h' style='width:${crtr_width}px'>Tiêu chí</th>`;
            var table_tbody = "";
            var univ_width = (containerWidth-ctgr_width-crtr_width)/selectedNum;
            $('#comp-univ-multiselect option:selected').each(function(){
                let tmp = $(this).text();
                let id = $(this).val();
                univ_table_th += `<th class="comp__univ_table-${id}-h comp__univ_table-uni-h" style="width:${univ_width}px">` + tmp + '</th>';
                scores_list_for_university_compare(parseInt(id));
            });
            $('#compare__university_table-th').html(univ_table_th);
            $($(this).attr('show')).animate({opacity:"show"},300);
            $('html, body').animate({scrollTop:$($(this).attr('show')).offset().top - 104}, 400);
        }
        else{
            $('html, body').animate({scrollTop:$('#compare__university_univ-selection').offset().top - 70}, 200);
            iziToast.error({
                title: 'Bạn phải chọn ít nhất 2 trường để so sánh!',
                position: 'bottomLeft',
            });
            $($(this).attr('show')).hide();   
        }
    });
    $(document).on('click touch', '.gs1-btn', function(){
        let sectorName = $(this).text();
        let sector_id = $(this).attr('id-gs1');
        // iziToast.info({
        //     title: `Đã chọn khối ngành ${sectorName}`,
        //     position: 'bottomLeft',
        // });
        $('#compare__subject_univ-selection').hide();
    	$('.gs1-btn').removeClass('btn-select');
    	$('.gs1-btn').find($('.fa')).removeClass('fa-check');
    	$(this).addClass('btn-select');
    	$(this).find($('.fa')).addClass('fa-check');
    	$('#subject-area').html('<div class="alert alert-warning mx-auto mt-3 h-25">Bạn chưa chọn nhóm ngành</div>');

    	//request for group
        let url = `/api/v1/sectors/${sector_id}/subjects`;
        ajax_request(false, true, "GET", "json", url, null, null, group_success_callback, error_callback);
    });
    $(document).on('click touch', '.gs2-btn', function(){
        let groupName = $(this).text();
        let group_id = $(this).attr('id-gs2');
        // iziToast.info({
        //     title: `Đã chọn nhóm ngành ${groupName}`,
        //     position: 'bottomLeft',
        // });
        $('#compare__subject_univ-selection').hide();
    	$('.gs2-btn').removeClass("btn-select");
    	$('.gs2-btn').find($('.fa')).removeClass('fa-check');
    	$(this).addClass('btn-select');
    	$(this).find($('.fa')).addClass('fa-check');

        let subject_list = $(groups_list).filter(function(index, groups){
            if(groups.group.id == group_id) return groups;
        });
        subjects_list_of_group(subject_list[0].subjects);
    });
    $(document).on('click touch', '.subject-btn', function(){
        let subjectName = $(this).attr('subject-name');
        // iziToast.info({
        //     title: `Đã chọn ngành ${subjectName}`,
        //     position: 'bottomLeft',
        // });
        let $this = $(this);
        $('#compare__subject_subj-selection').hide();
        $('#compare__subject_univ-selection').hide().animate({opacity: "show"}, 200, function(){
            scroll_to_id($this);
        });
        $('#univ-next-btn').removeClass('disabled');
        $('.subject-btn').removeClass('btn-select');
    	$(this).addClass('btn-select');
    	$('.subject-btn').find($('.fa')).removeClass('fa-check');
    	$(this).find($('.fa')).addClass('fa-check');
    	$('#c-s-tit-31').text('Chọn trường ngành ' + subjectName);
	    $('#selected-subject').html('Chọn trường cần so sánh ngành ' +  subjectName + ': ');
	    $('#compare__subject_table-title').text('So sánh ngành ' + subjectName);
        let subject_selected_id = parseInt($(this).attr('subject-id'));
        subjectId = subject_selected_id;

        //AJAX request
        let url = '/api/v1/universities';
        let data = {
            subject : subject_selected_id,
        };
        ajax_request(false, true, "GET", "json", url, null, data, universities_success_callback, error_callback);
    });
    $(document).on('click touch', '.gs-btn', function(){
    	$('#compare__subject-table').hide();
        subj_table_th ="<th>Nhóm tiêu chí</th><th>Tiêu chí</th>";
    });

    $(document).on('click touch', '.comp__subj_table-category', function(){
       let ctgr_id = $(this).attr('ctgr-id');
       if(subj_display){
           $(`.subj__ctgr_${ctgr_id}-row`).hide();
           $(this).find('.fa').removeClass('fa-minus-circle').removeClass('text-warning').addClass('fa-plus-circle').addClass('text-success');
           subj_display = false;
       }
       else{
           $(`.subj__ctgr_${ctgr_id}-row`).show();
           $(this).find('.fa').removeClass('fa-plus-circle').removeClass('text-success').addClass('fa-minus-circle').addClass('text-warning');
           subj_display = true;
       }
    });

    $(document).on('click touch', '.comp__univ_table-category', function(){
        let ctgr_id = $(this).attr('ctgr-id');
        if(univ_display){
            $(`.univ__ctgr_${ctgr_id}-row`).hide();
            $(this).find('.fa').removeClass('fa-minus-circle').removeClass('text-warning').addClass('fa-plus-circle').addClass('text-success');
            univ_display = false;
        }
        else{
            $(`.univ__ctgr_${ctgr_id}-row`).show();
            $(this).find('.fa').removeClass('fa-plus-circle').removeClass('text-success').addClass('fa-minus-circle').addClass('text-warning');
            univ_display = true;
        }
    });

    //AJAX FUNCTION

    function error_callback(response){
    	alert("Đã xảy ra lỗi, xem response tại console");
    }
    
    function group_success_callback(response){
        let groups = response.sorted_subjects; groups_list = groups;
        let pane = "";
        $.each(groups, function(index, group){
           pane += `<div class="col-md-6 h-25"><btn show="#compare__subject_subj-selection" class="btn gs-btn gs2-btn go-to-id" id="gs-2-${group.group.id}" id-gs2="${group.group.id}"><i class="fa mt-1 right-icon"></i>${group.group.name}</btn></div>`;
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
            pane += `<div class="col-md-6 h-25"><btn show="#compare__subject_univ-selection" class="btn gs-btn subject-btn go-to-id" id="subject-${subject.id}" subject-name="${subject.name}" subject-id="${subject.id}"><i class="fa mt-1 right-icon"></i> ${subject.name}</btn></div>`;
        });
        $('#subject-area').html(pane);
        $('#tab2, #groupSubject-2').removeClass('active');
        $('#tab3').addClass('active');
        $('#subject').removeClass('fade');
        $('#subject').addClass('active');
    };

    function universities_success_callback(response){
        let universities = response.universities;
        let pane = "";

        $.each(universities, function(index, university){
            pane += `<option univ-name="${university.name}" value="${university.id}">${university.name}</option>`;
        });
        $('#comp-subj-multiselect').html(pane);
        $('#comp-subj-multiselect').chosen({max_selected_options: 5});
        $(".search-choice").remove();

        $('.subject__selected-box').html('Bạn chưa chọn trường nào!');
        $('#comp-subj-multiselect').trigger('chosen:updated');
        $('#comp-subj-multiselect').bind("chosen:maxselected", function(){    
            iziToast.destroy();
            iziToast.warning({
                title: 'Bạn đã chọn đủ số trường tối đa là 5 trường!',
                position: 'bottomLeft',
            });
        });
    };

    function all_universities_success_callback(response){
        let universities = response.universities;
        let pane = "";

        $.each(universities, function(index, university){
            pane += `<option univ-name="${university.name}" value="${university.id}">${university.name}</option>`;
        });
        
        $('#comp-univ-multiselect').html(pane);
        $('#comp-univ-multiselect').chosen({max_selected_options: 5});
        $('.search-choice, .university__selected-box p').remove();

        $('.university__selected-box').html('Bạn chưa chọn trường nào !!');
        $('#comp-univ-multiselect').trigger('chosen:updated');
        $('#comp-univ-multiselect').bind("chosen:maxselected", function(){
            iziToast.destroy();
            iziToast.warning({
                title: 'Bạn đã chọn đủ số trường tối đa là 5 trường!',
                position: 'bottomLeft',
            });
        });
    };

    $(document).on("change", "#comp-subj-multiselect", function(){
        selected_univ = [];
        let li_count = $("#comp_subj_multiselect_chosen .chosen-choices").find("li").length;
        let last_select_univ = $('#comp_subj_multiselect_chosen .chosen-choices').find('li').eq(li_count - 2).find('span').text();
        let univ_box = '';

        $("#comp-subj-multiselect option:selected").each(function(){
            let univ_name = $(this).attr('univ-name');
            let univ_id = $(this).val();
            let data = {
                id : univ_id,
                name : univ_name,
            };
            selected_univ.push(data);
        });
        iziToast.success({
            title: `Đã thêm ${last_select_univ} vào danh sách so sánh!`,
            position: 'bottomLeft',
        });
        $.each(selected_univ, function(index, university){  
            univ_box += `<p class="my-1 ml-0 mr-lg-4"><i title="Xóa khỏi danh sách" data-toggle="tooltip" class="fa fa-remove subject__remove-univ mr-4" target="${university.id}" target-name="${university.name}"></i> <a href="/university/${university.id}" target="_blank" data-toogle="tooltip" title="Xem thong tin ${university.name}"> ${university.name} </a> </p>`;
        });
        $(".subject__selected-box").html(univ_box);
    });

    $(document).on("change", "#comp-univ-multiselect", function(){
        selected_univ = [];
        let li_count = $("#comp_univ_multiselect_chosen .chosen-choices").find("li").length;
        let last_select_univ = $('#comp_univ_multiselect_chosen .chosen-choices').find('li').eq(li_count - 2).find('span').text();
        let univ_box = "";

        $('#comp-univ-multiselect option:selected').each(function(){
            let univ_name = $(this).attr('univ-name');
            let univ_id = $(this).val();
            let data = {
                id: univ_id,
                name: univ_name,
            };
            selected_univ.push(data);
        });
        iziToast.success({
            title: `Đã thêm ${last_select_univ} vào danh sách so sánh!`,
            position: 'bottomLeft',
        });
        $.each(selected_univ, function(index, university){
            univ_box += `<p class="my-1 ml-0 mr-xl-4"> <i title="Xóa khỏi danh sách" data-toggle="tooltip" class="fa fa-remove university__remove-univ mr-4" target="${university.id}" target-name="${university.name}"></i> <a class="" target="_blank" href="/university/${university.id}" data-toggle="tooltip" title="Xem thông tin ${university.name}"> ${university.name} </a> </p>`;
        });
        $('.university__selected-box').html(univ_box);
    });

    $(document).on("click touch", ".subject__remove-univ", function(){
        let id = $(this).attr('target');
        let name = $(this).attr('target-name');
        let values = $('#comp-subj-multiselect').val();
        if(values){
            let i = values.indexOf(id);
            if(i >= 0){
                values.splice(i, 1);
                $('#comp-subj-multiselect').val(values).change();
            }
        }
        iziToast.destroy();
        iziToast.warning({
            title: `Đã xóa ${name} khỏi danh sách so sánh!`,
            position: 'bottomLeft',
        });
        $('#comp-subj-multiselect').trigger("chosen:updated");
    });
    $(document).on('click touch', '.university__remove-univ', function(){
        let id = $(this).attr('target');
        let name = $(this).attr('target-name');
        let values = $('#comp-univ-multiselect').val();
        if(values){
            let i = values.indexOf(id);
            if(i >= 0){
                values.splice(i, 1);
                $('#comp-univ-multiselect').val(values).change();
            }
        }
        iziToast.destroy();
        iziToast.warning({
            title: `Đã xóa ${name} khỏi danh sách so sánh!`,
            position: 'bottomLeft',
        });
        $("#comp-univ-multiselect").trigger("chosen:updated");
    });

    function get_all_sector(){
        let url = "/api/v1/sectors";
        ajax_request(false, true, "GET", "json", url, null, null, all_sectors_success_callback, error_callback);
    };

    function all_sectors_success_callback(response){
        let sectors = response.sectors;
        let pane = "";
        $.each(sectors, function(index, sector){
            pane += `<div class="col-md-6 h-25"><btn show="#compare__subject_subj-selection" class="btn gs-btn gs1-btn go-to-id" id-gs1="${sector.id}"><i class="fa mt-1" style="float:right"></i> ${sector.name}</btn></div>`;
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
            ajax_request(false, true, "GET", "json", url, null, null, all_category_university_callback, error_callback);
        }
    };

    function all_category_subject_callback(response){
        let categories = response;
        subj_ctgrCrtr = categories;
    }

    function all_category_university_callback(response){
        univ_ctgrCrtr = response;
    }
    
    function scores_list_for_subject_compare(university_id, subject_id){
        let univ_id = university_id;
        let subj_id = subject_id;
        let url = `/api/v1/universities/${univ_id}/subjects/${subj_id}/scores`;
        let data = {
            university_id: university_id,
            subject_id : subject_id,
        };
        ajax_request(false, true, "GET", "json", url, null, data, score_list_subject_compare_success_callback, error_callback);
    }

    function score_list_subject_compare_success_callback(response){
        response_id = response.profile.university.id;
        score_list[`${response_id}`] = response.scores;

        let table_tbody = "";
        let colspan = $('#comp-subj-multiselect option:selected').length + 1;

        $.each(subj_ctgrCrtr, function(category_index, cCr){
            let tmp = '';
            let rowspan = Object.keys(cCr.criteria).length;
            let category = cCr.criterion_category;
            let crs = cCr.criteria;

            table_tbody += `<tr><td class="text-left comp__subj_table-category" ctgr-id="${category.id}" colspan='${colspan}'>${category.name} <i class="right-icon sm-icon text-warning fa fa-minus-circle"></i></td></tr>`;

            $.each(crs, function(criterion_index, cr){
                table_tbody +=  `<tr class="subj__ctgr_${category.id}-row">` + `<td class="comp__subj_table-criterion">${cr.name} <i class="right-icon sm-icon fa fa-info-circle"></i></td>`;
                let uni_index = 0; let cr_id = cr.id;
                jQuery('#comp-subj-multiselect option:selected').each(function(){
                    let id = parseInt($(this).val());
                    let score = "Chưa có dữ liệu!";
                    
                    if(score_list[id] != undefined) {
                        if(score_list[id].length != 0){
                            $(score_list[id][category_index].criterion_scores).filter(function(i, criterion_score){
                                if(criterion_score.criterion.id == cr_id){
                                    score = criterion_score.score;
                                }
                            });
                        }
                        else score = "Chưa có dữ liệu!";
                    }
                    else score = "Chưa có dữ liệu!";
                    table_tbody += `<td class="comp__subj_table-${id} comp__subj_table-cr-${cr.id} comp__subj_score-ctgr-${category.id}">${score} <i class="fa" style="color:yellow"></i></td>`;
                    uni_index += 1;
                });
                table_tbody += '</tr>';
            });
        });
        setData(table_tbody, function(){
            setWidth(function(){
                highestScore();
            })
        });

        function setData(tbody, callback){
            jQuery('#compare__subject_table-tbody').html(tbody);
            callback();
        };

        function setWidth(callback){
            jQuery('#comp-subj-multiselect option:selected').each(function(){
                let id = $(this).val();
                let width = $(`.subject-univ-${id}`).width();

                $(`.comp__subj_table-${id}`).width(width);
            });

            $('.comp__subj_table-criterion').width($('.comp__subj_table-criterion-h').width());
            callback();
        }
        function highestScore(){
            $.each(subj_ctgrCrtr, function(index, cCr){
                let crs = cCr.criteria;
                $.each(crs, function(index, cr){
                    var high = 0;
                    $(`.comp__subj_table-cr-${cr.id}`).each(function(){
                        let num = parseFloat($(this).text());
                        if(num >= high) high = num;
                    });
                    $(`.comp__subj_table-cr-${cr.id}`).each(function(){
                        let num = parseFloat($(this).text());
                        if(num == high){
                            $(this).find($('.fa')).addClass('fa-star');
                            $(this).addClass('highest');
                        }
                    });
                });
            });
        }
    };

    function scores_list_for_university_compare(university_id){
        let uni_id = university_id;
        let url = `/api/v1/universities/${uni_id}/scores`;
        let data = {
            university_id : university_id,
        };
        ajax_request(false, true, "GET", "json", url, null, data, score_list_university_compare_success_callback, error_callback);
    }

    function score_list_university_compare_success_callback(response){
        response_id = response.profile.university.id;
        let table_tbody = "";
        let colspan = $('#comp-univ-multiselect option:selected').length + 1;
        score_list[`${response_id}`] = response.scores;

        $.each(univ_ctgrCrtr, function(category_index, cCr){
            let tmp = '';
            let category = cCr.criterion_category;
            let crs = cCr.criteria;
            table_tbody += `<tr><td class="text-left comp__univ_table-category" ctgr-id="${category.id}" colspan='${colspan}'>${category.name}<i class="right-icon sm-icon text-warning fa fa-minus-circle"></i></td></tr>`;

            $.each(crs, function(criterion_index, cr){
                table_tbody +=  `<tr class="univ__ctgr_${category.id}-row">` + `<td class="comp__univ_table-criterion">${cr.name} <i class="right-icon sm-icon fa fa-info-circle"></i></td>`;
                let uni_index = 0; let cr_id = cr.id;
                jQuery('#comp-univ-multiselect option:selected').each(function(){
                    let id = parseInt($(this).val());
                    let score = "Chưa có dữ liệu!";
                    if(score_list[id] != undefined) {
                        if(score_list[id].length != 0){
                            $(score_list[id][category_index].criterion_scores).filter(function(i, criterion_score){
                                if(criterion_score.criterion.id == cr_id){
                                    score = criterion_score.score;
                                }
                            });
                        }
                        else score = "Chưa có dữ liệu!";
                    }
                    else score = "Chưa có dữ liệu!";
                    table_tbody += `<td class="comp__univ_table-${id} comp__univ_table-cr-${cr.id} comp__univ_score-ctgr-${category.id}">${score} <i class="fa" style="color:yellow"></i></td>`;
                    uni_index += 1;
                });
                table_tbody += '</tr>';
            });
        });

        setData(table_tbody, function(){
            setWidth(function(){
               highestScore();
            });
        });
        
        function setData(tbody, callback){
            jQuery('#compare__university_table-tbody').html(tbody);
            callback();
        };

        function setWidth(callback){
            jQuery('#comp-univ-multiselect option:selected').each(function(){
                let id = $(this).val();
                let width = $(`.comp__univ_table-${id}-h`).width();

                $(`.comp__univ_table-${id}`).width(width);
            });

            $('.comp__univ_table-criterion').width($('.comp__univ_table-criterion-h').width());
            callback();
        };

        function highestScore(){
            $.each(univ_ctgrCrtr, function(index, cCr){
                let crs = cCr.criteria;
                $.each(crs, function(index, cr){
                    var high = 0;
                    $(`.comp__univ_table-cr-${cr.id}`).each(function(){
                        let num = parseFloat($(this).text());
                        if(num >= high) high = num;
                    });

                    $(`.comp__univ_table-cr-${cr.id}`).each(function(){
                        let num = parseFloat($(this).text());
                        if(num == high){
                            $(this).find($('.fa')).addClass('fa-star');
                            $(this).addClass('highest');
                        }
                    });
                });
            });
        }
    };

    //Fix a div to top after scroll over it. Now it has a bug !!!!!!!!!!!!!!!!!!
    // $(window).scroll(function(){
    //     if($(window).scrollTop() >= $('.fix-on-scroll').offset().top){
    //         $('.fix-on-scroll').css({
    //             position:'fixed',
    //             top: '72px',
    //             left: '77px',

    //             'z-index': "100",

    //         });
    //     }
    //     else{
    //         $('.fix-on-scroll').css({
    //             position: 'absolute',
    //         });
    //     }
    // });

    // setTimeout( function(){
        // console.log($('#compare__subject-table').html());
    // }, 30000)
});



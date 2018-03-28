jQuery(document).ready(function(){
	jQuery('#subject-compare').click(function(){
		jQuery('#select-21, #step-2').css({"display":"block"});
		jQuery('#select-22, #select-23, #select-32, #select-33, #table-2, #table-3').css({"display":"none"});

	});
	jQuery('#university-compare').click(function(){
		jQuery('#select-21, #select-23, #select-31, #select-33, #table-1, #table-3').hide();
		jQuery('#select-22, #step-2').show();

	});
    // jQuery('#university-compare').click(function(){
    //     jQuery('#select-21, #select-22, #select-31, #select-32, #table-2, #table-3').hide();

    //     jQuery('#select-23, #step-2').show();
    // });    
    jQuery('#btn-23').click(function(){jQuery('#select-33').show();});
    jQuery(document).on('click', '.btn-2', function(){
    	jQuery('.btn-2').removeClass("btn-select");
    	jQuery(this).addClass("btn-select");
    	jQuery('#select-31').show();
    });
    jQuery('.btn-3').click(function(){
    	jQuery(this).toggleClass('btn-select');
    });
    jQuery('.btn-22').click(function(){
    	jQuery('.btn-22').removeClass("btn-select");
    	jQuery(this).toggleClass("btn-select");
    	jQuery('#select-32').show();
    });
    var table_th_1 ="";
    var caCr = [];
    jQuery("#compare-btn-31").click(function(){
    	// jQuery('#DataTables_Table_0_length label').contents().first()[0].textContent="Số trường trên bảng: ";
    	// jQuery('#DataTables_Table_0_length label').contents().last()[0].textContent=" trường."
    	// jQuery('#DataTables_Table_0_filter label').contents().first()[0].textContent="Tìm kiếm: ";
    	// jQuery('a[data-dt-idx="0"]').text("Trang trước");
    	// jQuery('a[data-dt-idx="8"]').text("Trang sau");
    	// let Info = jQuery("#DataTables_Table_0_info");
    	// Info.html(Info.html().replace("Showing", "Đang thể hiện trên bảng từ trường số "));
    	// Info.html(Info.html().replace("to", " tới trường số "));
    	// Info.html(Info.html().replace("of", " trên tổng số "));
    	// Info.html(Info.html().replace("entries", " trường."));
        var containerWidth = $('.container').width();
        var selectedNum = $('#mul-s-31 :selected').length;
        var w1 = 161; var w2 = 171;
        table_th_1 =`<th class='c-t-s-category-h' style='width:${w1}px'>Nhóm tiêu chí</th><th class='c-t-s-criterion-h' style='width:${w2}px'>Tiêu chí</th>`;
        var table_tbody = "";
        // var containerWidth = $('.container').width();
        // var selectedNum = $('#mul-s-31 :selected').length;
        var w = (containerWidth-w1-w2)/selectedNum;
        $('#mul-s-31 option:selected').each(function(){
            let tmp = $(this).text();
            let id = $(this).val();
            table_th_1 += `<th class="c-t-s-${id}-h c-t-s-uni-h" style="width:${w}px">` + tmp + '</th>';
        });
        $('#uni-selected-t-1').html(table_th_1);
        $.each(caCr, function(index, cCr){
            let tmp = '';
            table_tbody += `<tr><td class="c-t-s-category c-t-s-ca-${cCr.id}" rowspan='${Object.keys(cCr.criteria).length}'>${cCr.name}</td>`;
            let crs = cCr.criteria;

            $.each(crs, function(index, cr){
                table_tbody +=  tmp + `<td class="c-t-s-criterion c-t-s-${cCr.id}-cr">${cr.name}</td>`;
                jQuery('#mul-s-31 option:selected').each(function(){
                    let id = $(this).val();
                    // table_th_1 += '<th>'+ txt + '</th>';
                    table_tbody += `<td class="c-t-s-${id} c-t-s-${cr.id}">9.0 <i class="fa" style="color:yellow"></i></td>`;
                });
                tmp = '<tr>';
                table_tbody += '</tr>';

            });
            
        });
        
        jQuery('#c-s-tbody-1').html(table_tbody);
        
        setWidth();
        function setWidth(){
            jQuery('#mul-s-31 option:selected').each(function(){
                let id = $(this).val();
                let width = $(`.c-t-s-${id}-h`).width();
                
                $(`.c-t-s-${id}`).width(width);
            });
        }
        $('.c-t-s-category').width($('.c-t-s-category-h').width()-1);
        $('.c-t-s-criterion').width($('.c-t-s-criterion-h').width());
        // $('.sortable').DataTable();
        $.each(caCr, function(index, cCr){
            let crs = cCr.criteria;
            $.each(crs, function(index, cr){
                var high = 0;
                $(`.c-t-s-${cr.id}`).each(function(){
                    let num = parseInt($(this).text());
                    if(num >= high) high = num;
                });

                $(`.c-t-s-${cr.id}`).each(function(){
                    let num = parseInt($(this).text());
                    if(num === high){
                        $(this).find($('.fa')).addClass('fa-star');
                        $(this).css("font-size","19px");
                        $(this).addClass('highest');
                    }
                });
            });
        });
    });

    var groups_json;
    get_all_sector();
    get_university_list();
    get_all_category('subject');
    
    // Compare-table-by-university

    $('.multiple-uni-select').select2({maximumSelectionLength: 5});
    var table_th_2 = ""; var caCr_u = [];
    get_all_category('university');
    jQuery(document).on('click', '#c-btn-2-2', function(){
        var containerWidth = $('.container').width();
        var selectedNum = $('#mul-s-22 :selected').length;
        var w1 = 161; var w2 = 171;
        table_th_2 =`<th class='c-t-u-category-h' style='width:${w1}px'>Nhóm tiêu chí</th><th class='c-t-u-criterion-h' style='width:${w2}px'>Tiêu chí</th>`;
        var table_tbody = "";
        // var containerWidth = $('.container').width();
        // var selectedNum = $('#mul-s-31 :selected').length;
        var w = (containerWidth-w1-w2)/selectedNum;
        $('#mul-s-22 option:selected').each(function(){
            let tmp = $(this).text();
            let id = $(this).val();
            table_th_2 += `<th class="c-t-u-${id}-h c-t-u-uni-h" style="width:${w}px">` + tmp + '</th>';
        });
        $('#uni-selected-t-2').html(table_th_2);
        $.each(caCr_u, function(index, cCr){
            let tmp = '';
            table_tbody += `<tr><td class="c-t-u-category c-t-u-ca-${cCr.id}" rowspan='${Object.keys(cCr.criteria).length}'>${cCr.name}</td>`;
            let crs = cCr.criteria;

            $.each(crs, function(index, cr){
                table_tbody +=  tmp + `<td class="c-t-u-criterion c-t-u-${cCr.id}-cr">${cr.name}</td>`;
                jQuery('#mul-s-22 option:selected').each(function(){
                    let id = $(this).val();
                    // table_th_1 += '<th>'+ txt + '</th>';
                    table_tbody += `<td class="c-t-u-${id} c-t-u-${cr.id}">9.0 <i class="fa" style="color:yellow"></i></td>`;
                });
                tmp = '<tr>';
                table_tbody += '</tr>';

            });
            
        });
        
        jQuery('#c-u-tbody-2').html(table_tbody);
        
        setWidth();
        function setWidth(){
            jQuery('#mul-s-22 option:selected').each(function(){
                let id = $(this).val();
                let width = $(`.c-t-u-${id}-h`).width();
                
                $(`.c-t-u-${id}`).width(width);
            });
        }
        $('.c-t-u-category').width($('.c-t-u-category-h').width()-1);
        $('.c-t-u-criterion').width($('.c-t-u-criterion-h').width());
        // $('.sortable').DataTable();
        $.each(caCr_u, function(index, cCr){
            let crs = cCr.criteria;
            $.each(crs, function(index, cr){
                var high = 0;
                $(`.c-t-u-${cr.id}`).each(function(){
                    let num = parseInt($(this).text());
                    if(num >= high) high = num;
                });

                $(`.c-t-u-${cr.id}`).each(function(){
                    let num = parseInt($(this).text());
                    if(num === high){
                        $(this).find($('.fa')).addClass('fa-star');
                        $(this).css("font-size","19px");
                        $(this).addClass('highest');
                    }
                });
            });
        });

    	// table_u_body ="";
    	// jQuery('#mul-s-22 option:selected').each(function(){
    	// 	let txt = $(this).text();
    	// 	table_u_body += '<tr><td>'+ txt + '</td><td>8.9</td><td>9.0</td><td>8.7</td><td>9.3</td><td>9.5</td></tr>';
    	// });
    	// jQuery('#table-u-body').html(table_u_body);
    });
    jQuery(document).on('click', '.gs1-btn', function(){
    	jQuery('#select-31').hide();
    	jQuery('.gs1-btn').removeClass('btn-select');
    	$('.gs1-btn').find($('.fa')).removeClass('fa-check');
    	jQuery(this).addClass('btn-select');
    	$(this).find($('.fa')).addClass('fa-check');
    	let sector_id = $(this).attr('id-gs1');
    	$('#subject-area').html('<div class="alert alert-warning mx-auto mt-3">Bạn chưa chọn nhóm ngành</div>');
    	// update_sector_choice(sector_id);
        let url = `/api/sectors/${sector_id}/subjects`;
        ajax_request(false, true, "GET", "json", url, null, null, group_success_callback, error_callback);
    });
    jQuery(document).on('click', '.gs2-btn', function(){
    	jQuery('#select-31').hide();
    	jQuery('.gs2-btn').removeClass("btn-select");
    	$('.gs2-btn').find($('.fa')).removeClass('fa-check');
    	jQuery(this).addClass('btn-select');
    	$(this).find($('.fa')).addClass('fa-check');
    	let group_id = $(this).attr('id-gs2');
    	// update_group_choice(group_id);
        let subject_list = jQuery(groups_json).filter(function(index, entry){
            if(entry.id == group_id) return entry;
        });
        subjects_list_of_group(subject_list[0].subjects);
    });
    jQuery(document).on('click', '.subject-btn', function(){
    	jQuery('.subject-btn').removeClass('btn-select');
    	jQuery(this).addClass('btn-select');
    	$('.subject-btn').find($('.fa')).removeClass('fa-check');
    	$(this).find($('.fa')).addClass('fa-check');
    	let subjectName = $(this).attr('id-subject');
        $('#c-s-tit-31').text('Bạn muốn so sánh những trường nào trong ngành ' + subjectName + '?');
    	$('#c-s-table-title').text('So sánh ngành ' + subjectName);
    });
    jQuery(document).on('click', '.gs-btn', function(){
    	jQuery('#table-1').hide();

        table_th ="<th>Nhóm tiêu chí</th><th>Tiêu chí</th>";
    });
    function error_callback(response){
    	alert("Đã xảy ra lỗi, xem response tại console");
    }
    
    function group_success_callback(response){
    	
        let groups = response.groups; groups_json = groups;
        let pane = "";
        $.each(groups, function(index, group){
           pane += `<div class="col-md-4"><a href="#select-21" show="#select-21" class="btn gs-btn gs2-btn go-to-id" id="gs-2-${group.id}" id-gs2="${group.id}">${group.name}<i class="fa mt-1" style="float:right"></i></a></div>`; 
       });
        $('#gs2-area').html(pane);
        $('#tab1, #groupSubject-1').removeClass('active');
        $('#tab2').addClass('active');
        $('#groupSubject-2').removeClass('fade');
        $('#groupSubject-2').addClass('active');

    }

    // function update_group_choice(group_id){
    //     let url = "/api/allSubjects";
    //     ajax_request(false, true, "GET", "json", url, null, null, subject_success_callback, error_callback);
    // }
    function subjects_list_of_group(subjects){
    	let pane = "";
        $.each(subjects, function(index, subject){
            pane += `<div class="col-md-4"><a show="#select-31" href="#select-31" class="btn gs-btn subject-btn go-to-id" id="subject-${subject.id}" id-subject="${subject.name}">${subject.name}<i class="fa mt-1" style="float:right"></i></a></div>`;
        });
        $('#subject-area').html(pane);
        $('#tab2, #groupSubject-2').removeClass('active');
        $('#tab3').addClass('active');
        $('#subject').removeClass('fade');
        $('#subject').addClass('active');
    };
    function get_university_list(){
    	let url = "/api/allUniversity";
    	ajax_request(false, true,  "GET", 'json', url, null, null, all_universities_success_callback, error_callback);
    }
    function all_universities_success_callback(response){
        let universities = response.universities;
        let pane = "";
        $.each(universities, function(ỉndex, university){
            pane += `<option value="${university.id}">${university.name}</option>`;
        });
        $('.multiple-uni-select').html(pane);
    };
    function get_all_sector(){
        let url = "/api/sectors";
        ajax_request(false, true, "GET", "json", url, null, null, all_sectors_success_callback, error_callback);
    };
    function all_sectors_success_callback(response){
        let sectors = response.sectors;
        let pane = "";
        $.each(sectors, function(index, sector){
            pane += `<div class="col-md-4"><a show="#select-21" class="btn gs-btn gs1-btn go-to-id" href="#select-21" id-gs1="${sector.id}">${sector.name}<i class="fa mt-1" style="float:right"></i></a></div>`;
        });
        $("#gs1-area").html(pane);

    }

    function get_all_category(target){
        let url = "/api/categories";
        let data = {
            target : target,
        };
        if(target == "subject"){
            ajax_request(false, true, "GET", "json", url, null, data, all_category_subject_callback, error_callback);
        }
        else if(target == "university"){
            ajax_request(false, true, "GET", "json", url, null, data, all_category_university_callback, error_callback);
        }
    }
    function all_category_subject_callback(response){
        let categories = response.categories; caCr = categories;
        $.each(categories, function(index, category){
            console.log(Object.keys(category.criteria).length);
        });
    }
    function all_category_university_callback(response){
        caCr_u = response.categories;
    }
});


    //);

    // });
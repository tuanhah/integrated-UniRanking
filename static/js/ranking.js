jQuery(document).ready(function(){         
    // $(window).resize(function(){
    //     var img_width = $('.background-img').parent().width();
    //     $('.background-img').css({'width':img_width});
    // });


    var scard = $('.selection-card');
    var fcard = $('.fixed-card');
    var scard_pos = scard.position();
    var select_area = $('.select-area');

    iziToast.settings({
        timeout: 2500,
    });
    
    $(window).scroll(function () {
        if($('#ranking__university-table').css('display') == "none" && $('#ranking__subject-table').css('display') == "none" && $(window).width() >= 992) {
            var window_pos = $(window).scrollTop();
            var select_area_height = select_area.height();

            if (window_pos + 60 >= scard_pos.top && window_pos + 60 + fcard.height() <= select_area.position().top + select_area_height) {
                $('.fixed-card').addClass('fixed--after-menu');
            }
            else {
                $('.fixed-card').removeClass('fixed--after-menu');
            }
        }
        else $('.fixed-card').removeClass('fixed--after-menu');
    });

    jQuery(document).on('click touch', '#subject-ranking', function(){
        iziToast.info({
            title: 'Đã chọn xếp hạng theo ngành!',
            position: 'bottomLeft',
        });
        let $this = $(this);
        $('#subject-ranking i').remove();
        $('#subject-ranking, #university-ranking').removeClass('text-left');
        $(this).addClass('text-left').prepend(' <i class="fa fa-check-circle md-icon float-right"></i>');
        $('#university-ranking i').remove();
        jQuery('#ranking__subject_subj-selection, #step-2').hide().animate({opacity:'show'}, 200, function(){
            scroll_to_id($this);
        });
        jQuery('#ranking__university_univ-selection, #ranking__university-table, #ranking__university-table, #carousel-rank-area').hide();
        get_all_sector();
        get_all_category('subject');
        
    });
    var univ_th_ctgr;
    var univ_th_crtr;
    var univ_th_sort;
    var subjTablData = new Array();
    var univTablData = new Array();
    var widthArray = new Array(); 
    var univ_table_body = '';
    jQuery(document).on('click touch', '#university-ranking', function(){
        iziToast.info({
            title: 'Đã chọn xếp hạng theo trường!',
            position: 'bottomLeft',
        });
        univ_th_ctgr = '';
        univ_th_crtr = '';
        univ_th_sort = '';
        // let universities = [];

        $('#subject-ranking, #university-ranking').removeClass('text-left');
        $('#university-ranking i').remove();
        $(this).addClass('text-left').prepend(' <i class="fa fa-check-circle md-icon float-right"></i>');
        $('#subject-ranking i').remove();
        let $this = $(this);

        jQuery('#ranking__subject_subj-selection, #ranking__subject_univ-selection, #ranking__subject-table, #ranking__university-table').hide();
        jQuery('#ranking__university_univ-selection, #carousel-rank-area').hide().animate({opacity:'show'}, 200, function(){
            scroll_to_id($this);
        });
        function university_rank(){
            let url = '/api/v1/rank/university';
            let data = {
                //data here
            };
            ajax_request(false, true, "GET", "json", url, data, null, universities_ranking_success_callback, error_callback);
        }
        get_all_category('university');




        $('.loader-img').fadeIn(200).delay(800).animate({height:"hide"},300);
        set_table_title(function(){
            university_rank();
        });
        function set_table_title(callback){
            var containerWidth = $('.rank_table').width();
            var num_of_ctgr = 5;
            let univ_width = 350;
            let rank_width = 63;
            let number_of_crtr = 3;
            univ_th_ctgr =`<th rowspan="2" class="univ-rank-th bg-custom-2" style="width:${rank_width}px">Thứ hạng</th><th class='rank__univ_table-category-h bg-custom-2' rowspan="2    " style='width:${univ_width}px'>Trường</th>`;
            var ctgr_width = (containerWidth-rank_width-univ_width)/num_of_ctgr;
            univ_th_sort = '<th>s</th><th>s</th>';
            $.each(univ_ctgrCrtr, function(ctgr_index, ctgr){
                let colspan = Object.keys(ctgr.criteria).length;
                let category = ctgr.criterion_category;
                univ_th_ctgr += `<th class="comp__univ_table-category comp__univ_table-ctgr-${category.id}" colspan="${number_of_crtr}">${category.name}</th> `;
                let crtrs = ctgr.criteria;
                $.each(crtrs, function(crtr_index, crtr){
                    if(crtr_index <= number_of_crtr - 1){
                        univ_th_crtr += `<th class="comp__univ_table-criterion comp__univ_table-${category.id}-cr" criterion-id="${crtr.id}">${crtr.name}</th>`;
                        univ_th_sort += '<th>s</th>';
                    }
                });
            });
            $('#university_table_th-ctgr').html(univ_th_ctgr);
            $('#university_table_th-crtr').html(univ_th_crtr);
            $('#university_table_th-sort').html(univ_th_sort);

            callback();
        }	


        // function set_data_title(callback) {   
        //     $('#university_table_th-ctgr').html(univ_th_ctgr);
        //     $('#university_table_th-crtr').html(univ_th_crtr);
        //     $('#university_table_th-sort').html(univ_th_sort);
        // };

        // $($(this).attr('show')).animate({opacity:"show"},1000, function(){
        //     scroll_to_id()
        // });
        // $('html, body').animate({scrollTop:$($(this).attr('show')).offset().top - 104}, 1000);
    });
    
    var subj_table_th ="";
    var subj_ctgrCrtr = [];
    var ctgr_with_criterions = [];
    var scores = [];
    var score_list = [];
    var crtr_width =171;
    
    
    var groups_list;
    var univ_table_th = ""; var univ_ctgrCrtr = [];
    jQuery(document).on('click touch', '.gs1-btn', function(){
        let sectorName = $(this).text();
        iziToast.info({
            title: `Đã chọn khối ngành ${sectorName}!`,
            position: 'bottomLeft',
        });
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
    jQuery(document).on('click touch', '.gs2-btn', function(){
        let groupName = $(this).text();
        iziToast.info({
            title: `Đã chọn nhóm ngành ${groupName}!`,
            position: 'bottomLeft',
        });
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
    jQuery(document).on('click touch', '.subject-btn', function(){
        let subjectName = $(this).attr('subject-name');
        let $this = $(this);
        iziToast.info({
            title: `Đã chọn ngành ${subjectName}!`,
            position: 'bottomLeft',
        });
        jQuery('.subject-btn').removeClass('btn-select');
        jQuery(this).addClass('btn-select');
        $('.subject-btn').find($('.fa')).removeClass('fa-check');
        $(this).find($('.fa')).addClass('fa-check');
        $('#ranking__subject_table-title').text('So sánh ngành ' + subjectName);
        let subject_selected_id = parseInt($(this).attr('subject-id'));
        
        var subj_th_ctgr = '';
        var subj_th_crtr = '';
        var subj_th_sort = '';
        subjTablData = [];
        widthArray = [];
        table_title_data(subj_ctgrCrtr, function(){
            get_subject_ranking();
            
        })
        function get_subject_ranking(){
            let url = `/api/v1/rank/subject/${subject_selected_id}`;
            let data = {
                subject: subject_selected_id,
            }
            ajax_request(false, true, "GET", "json", url, null, data, subject_ranking_success_callback , error_callback);
        }

        
        $('.loader-img').fadeIn(200).delay(800).animate({height:"hide"},300);
        function table_title_data(array_of_ctgr, callback){
            var containerWidth = $('.rank_table').width();
            var num_of_ctgr = 4;
		    var num_of_crtr = 4;//$('#rank-subj-multiselect :selected').length;
		    let univ_width = 350;
            let rank_width = 63;
            subj_th_ctgr =`<th class="bg-custom-2" rowspan="2" style="width:${rank_width}px">Thứ hạng</th><th class='rank__subj_table-category-h bg-custom-2' rowspan="2" style='width:${univ_width}px'>Trường</th>`;
            var ctgr_width = (containerWidth-univ_width)/num_of_ctgr;
            subj_th_sort = '<th> </th><th> </th>';
            $.each(array_of_ctgr, function(ctgr_index, ctgr){
                let colspan = Object.keys(ctgr.criteria).length;
                let category = ctgr.criterion_category;
                subj_th_ctgr += `<th class="py-0 pr-0 ctgr comp__subj_table-category comp__subj_table-ctgr-${category.id}" colspan="${num_of_crtr}">${category.name}<btn class="px-2 py-1 btn change-crtr-btn" data-toggle="modal" data-target="#crtr-modal" ctgr-id="${category.id}"><i class="fa fa-plus"></i><btn></th>`;
                let crtrs = ctgr.criteria;
                $.each(crtrs, function(crtr_index, crtr){
                    if(crtr_index <= num_of_crtr - 1){
                       subj_th_crtr += `<th class="px-2 comp__subj_table-criterion comp__subj_table-${category.id}-cr" crtr-id="${crtr.id}" ctgr-id="${category.id}">${crtr.name}</th>`;
                       subj_th_sort += '<th> </th>';
                   }
               });
            });

            $('#subject_table_th-ctgr').html(subj_th_ctgr);
            $('#subject_table_th-crtr').html(subj_th_crtr);
            $('#subject_table_th-sort').html(subj_th_sort);
            
            callback();    
        }
        $($(this).attr('show')).animate({opacity:"show"},1000, function(){
            scroll_to_id($this);
        });
        
    });
    $(document).on('click touch', '.change-crtr-btn', function(){
        let id = $(this).attr('ctgr-id');
        let crtrs = [];
        let modal_body = '';
        $(subj_ctgrCrtr).filter(function(_i, element){
            if(element.criterion_category.id == id){
                crtrs = element.criteria;
            }
        });
        $.each(crtrs, function(index, crtr){
            modal_body += `<div class="checkbox"><label> <input type="checkbox" value="${crtr.id}"> ${crtr.name}</label></div>`;
        });
        $('#crtr-modal-body').html(modal_body);
    });

    function error_callback(response){
       alert("Đã xảy ra lỗi, xem response tại console");
    }
    function group_success_callback(response){

        let groups = response.sorted_subjects; groups_list = groups;
        let pane = "";
        $.each(groups, function(index, group){
        pane += `<div class="col-md-6"><btn show="#ranking__subject_subj-selection" class="btn gs-btn gs2-btn go-to-id" id="gs-2-${group.group.id}" id-gs2="${group.group.id}"><i class="fa mt-1 right-icon"></i> ${group.group.name}</btn></div>`;
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
        pane += `<div class="col-md-6"><btn show="#ranking__subject-table" class="btn gs-btn subject-btn go-to-id" id="subject-${subject.id}" subject-name="${subject.name}" subject-id="${subject.id}"><i class="fa mt-1 right-icon"></i> ${subject.name}</btn></div>`;
        });
        $('#subject-area').html(pane);
        $('#tab2, #groupSubject-2').removeClass('active');
        $('#tab3').addClass('active');
        $('#subject').removeClass('fade');
        $('#subject').addClass('active');
    };
    var univ_for_test = [];

    function universities_ranking_success_callback(response){
        let subjectRank = response.rank;
        univTablData = [];
        widthArray = [];

        get_data(subjectRank, function(){
            display_data(function(){
                width_setting();
                // Còn lỗi !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                // console.log(table);
                // if(table != undefined) {
                //     table.destroy();
                // }
                // table = $('.sort-table').DataTable({
                //     // "searching": false,
                //     // "lengthChange": false,
                //     "language":{
                //         "info": "Đang thể hiện từ trường số _START_ tới trường số _END_ trên tổng số _TOTAL_ trường",
                //         "lengthMenu": "Số trường trên bảng: _MENU_ trường.",
                //         "paginate" : {
                //             "next" : "Trang sau",
                //             "previous" : "Trang trước",
                //         },
                //         "search" : "Tìm kiếm: ",
                //     },
                //     "scrollY" : "50px",
                //     "scrollColapse" : "true",
                //     "data": univTablData,
                //     "autoWidth": true, 
                //     dom: 'Bfrtip',
                //     buttons: [
                //     'copyHtml5',
                //     'excelHtml5',
                //     'csvHtml5',
                //     'pdfHtml5',
                //         {
                //             text: 'Custom PDF',
                //             extend: 'pdfHtml5',
                //             filename: 'dt_custom_pdf',
                //             // orientation: 'landscape', //portrait
                //             pageSize: 'A4', //A3 , A5 , A6 , legal , letter
                //             exportOptions: {
                //                 columns: ':visible',
                //             // search: 'applied',
                //             // order: 'applied'

                //             },
                //             header: true,
                //             footer: true,
                //         },
                //     ]
                // });
                // $(".dataTables_scrollBody table thead:nth-child(3)").empty();
            });
        });
        function get_data(arrays, callback){
            arrays.forEach(function(univ, index){
                let university = univ.profile.university;
                let general_statistics = univ.profile.general_statistics;
                let univ_id = university.id;
                univTablData[index] = new Array();
                    univTablData[index].push(`${general_statistics.rank}`, `${university.name}`);// += `<tr><td class="subj-rank">${general_statistics.rank}</td><td class="subj__table_univ-name">${university.name}</td>`;
                    let scores = univ.scores;

                    for(let i = 0; i < 16; i++){
                        let crtr_id = $(`#subject_table_th-crtr th:nth-child(${i+1})`).attr('crtr-id');
                        let ctgr_id = parseInt($(`#subject_table_th-crtr th:nth-child(${i+1})`).attr('ctgr-id'));
                        let ctgr_index = parseInt(i/4);
                        let score = "n!"
                        if(scores.length != 0){
                            $(scores[ctgr_index].criterion_scores).filter(function(_i, param){
                                if(param.criterion.id == crtr_id){
                                    score = param.score;
                                }
                            });
                        }
                        else score = "n!";
                        univTablData[index].push(`${score}`); //+= `<td class="comp__subj_table-${univ_id} comp__subj_table-cr-${crtr_id} comp__subj_score-ctgr-${ctgr_id}">${score}</td>`;
                    }
                    // subjTablData += '</tr>';
                });
            callback();
        }
        function display_data(callback){
            callback();
        }
        function width_setting(){
            widthArray[0] = $(`#subject_table_th-ctgr th:nth-child(1)`).width();
            widthArray[1] = $(`#subject_table_th-ctgr th:nth-child(2)`).width();
            for(let i = 1; i <= 16; i++){
                widthArray[i+1] = $(`#subject_table_th-crtr th:nth-child(${i})`).width();
            }

        }
    }



    var selected_univ = [];


    function get_all_sector(){
        let url = "/api/v1/sectors";
        ajax_request(false, true, "GET", "json", url, null, null, all_sectors_success_callback, error_callback);
    };
    function all_sectors_success_callback(response){
        let sectors = response.sectors;
        let pane = "";
        $.each(sectors, function(index, sector){
            pane += `<div class="col-md-6"><btn show="#ranking__subject_subj-selection" class="btn gs-btn gs1-btn go-to-id" id-gs1="${sector.id}"><i class="fa mt-1" style="float:right"></i> ${sector.name}</btn></div>`;
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

        var scores_index = 0;
        var table;
        function subject_ranking_success_callback(response){
            let subjectRank = response.rank;
            subjTablData = [];
            widthArray = [];
            
            get_data(subjectRank, function(){
                display_data(function(){
                    width_setting();
                    if(table != undefined) {
                        table.destroy();
                    }
                    table = $('.sort-table').DataTable({
                        // "searching": false,
                        // "lengthChange": false,
                        "language":{
                            "info": "Đang thể hiện từ trường số _START_ tới trường số _END_ trên tổng số _TOTAL_ trường",
                            "lengthMenu": "Số trường trên bảng: _MENU_ trường.",
                            "paginate" : {
                                "next" : "Trang sau",
                                "previous" : "Trang trước",
                            },
                            "search" : "Tìm kiếm: ",
                        },
                        "pageLength": 25,
                        // "scrollY" : "200px",
                        // "scrollColapse" : true,
                        // "scrollX" : true,
                        "data": subjTablData,
                        "autoWidth": true, 

                        drawCallback: function () { // this gets rid of duplicate headers
                            $('.dataTables_scrollBody thead tr').css({height:'0px'});
                        },
                        // "initComplete": function(settings, json) {
                        //     $('.dataTables_scrollBody thead').css({height:'0px'});
                        // },
                        

                        // dom: 'Bfrtip',
                        // buttons: [
                        // 'copyHtml5',
                        // 'excelHtml5',
                        // 'csvHtml5',
                        // 'pdfHtml5',
                        // {
                        //     text: 'Custom PDF',
                        //     extend: 'pdfHtml5',
                        //     filename: 'dt_custom_pdf',
                        //     // orientation: 'landscape', //portrait
                        //     pageSize: 'A4', //A3 , A5 , A6 , legal , letter
                        //     exportOptions: {
                        //         columns: ':visible',
                        //     // search: 'applied',
                        //     // order: 'applied'

                        // },
                    //     header: true,
                    //     footer: true,
                    // },
                    // ]
                });
                    // $(".dataTables_scrollBody #subject_table_th-sort").empty();
                    
                });
            });
            function get_data(arrays, callback){
                arrays.forEach(function(univ, index){
                    let university = univ.profile.university;
                    let general_statistics = univ.profile.general_statistics;
                    let univ_id = university.id;
                    subjTablData[index] = new Array();
                    subjTablData[index].push(`${general_statistics.rank}`, `${university.name}`);// += `<tr><td class="subj-rank">${general_statistics.rank}</td><td class="subj__table_univ-name">${university.name}</td>`;
                    let scores = univ.scores;

                    for(let i = 0; i < 16; i++){
                        let crtr_id = $(`#subject_table_th-crtr th:nth-child(${i+1})`).attr('crtr-id');
                        let ctgr_id = parseInt($(`#subject_table_th-crtr th:nth-child(${i+1})`).attr('ctgr-id'));
                        let ctgr_index = parseInt(i/4);
                        let score = "n!";
                        if(scores.length != 0){
                            $(scores[ctgr_index].criterion_scores).filter(function(_i, param){
                                if(param.criterion.id == crtr_id){
                                    score = param.score;
                                }
                            });
                        }
                        else score = "n!";
                        subjTablData[index].push(`${score}`); //+= `<td class="comp__subj_table-${univ_id} comp__subj_table-cr-${crtr_id} comp__subj_score-ctgr-${ctgr_id}">${score}</td>`;
                    }
                    // subjTablData += '</tr>';
                });
                callback();
            }
            function display_data(callback){
                callback();
            }
            function width_setting(){
                widthArray[0] = $(`#subject_table_th-ctgr th:nth-child(1)`).width();
                widthArray[1] = $(`#subject_table_th-ctgr th:nth-child(2)`).width();
                for(let i = 1; i <= 16; i++){
                    widthArray[i+1] = $(`#subject_table_th-crtr th:nth-child(${i})`).width();
                }

            }
        }

        // function scores_list_for_university_ranking(university_id){
        //     let uni_id = university_id;
        //     let url = `/api/v1/universities/${uni_id}/scores`;
        //     let data = {
        //         university_id : university_id,
        //     };
        //     ajax_request(false, true, "GET", "json", url, null, data, score_list_university_ranking_success_callback, error_callback);
        // }
        // function score_list_university_ranking_success_callback(response){
        //     response_id = response.university_id;
        //     score_list[`${response_id}`] = response.score; 
        // }

    });
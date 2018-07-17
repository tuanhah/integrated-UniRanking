$(document).ready(function () {
    // $(window).resize(function(){
    //     var img_width = $('.background-img').parent().width();
    //     $('.background-img').css({'width':img_width});
    // });


    var scard = $('.selection-card');
    var fcard = $('.fixed-card');
    var scard_pos = scard.position();
    var select_area = $('.select-area');
    var category_length = 0;
    var subject_rank_universities = '';
    var university_rank_universities = '';

    $('#navibar').addClass('navbar__over');
    iziToast.settings({
        timeout: 2500,
    });

    get_all_sector();
    get_all_category('subject');


    jQuery(document).on('click touch', '#sector__ranking', function () {
        iziToast.info({
            title: 'Đã chọn xếp hạng theo ngành!',
            position: 'bottomLeft',
        });
        let $this = $(this);
        $('#subject-ranking i').remove();
        $('#subject-ranking, #university-ranking').removeClass('text-left');
        $(this).addClass('text-left').prepend(' <i class="fa fa-check-circle md-icon float-right"></i>');
        $('#university-ranking i').remove();
        jQuery('#ranking__subject_subj-selection, #step-2').hide().animate({
            opacity: 'show'
        }, 200, function () {
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
    jQuery(document).on('click touch', '#university-ranking', function () {
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
        jQuery('#ranking__university_univ-selection, #carousel-rank-area').hide().animate({
            opacity: 'show'
        }, 200, function () {
            scroll_to_id($this);
        });

        function university_rank() {
            let url = '/api/v1/rank/university';
            let data = {
                //data here
            };
            ajax_request(false, true, "GET", "json", url, data, null, universities_ranking_success_callback, error_callback);
        }
        get_all_category('university');

        $('.loader-img').fadeIn(200).delay(800).animate({
            height: "hide"
        }, 300);
        set_table_title(function () {
            university_rank();
        });

        function set_table_title(callback) {
            var containerWidth = $('.rank_table').width();
            var num_of_ctgr = 5;
            let univ_width = 350;
            let rank_width = 63;
            let number_of_crtr = 3;
            univ_th_ctgr = `<th rowspan="2" class="univ-rank-th bg-custom-2" style="width:${rank_width}px">Thứ hạng</th><th class='rank__univ_table-category-h bg-custom-2' rowspan="2" style='width:${univ_width}px'>Trường</th>`;
            var ctgr_width = (containerWidth - rank_width - univ_width) / num_of_ctgr;
            univ_th_sort = '<th>s</th><th>s</th>';
            $.each(univ_ctgrCrtr, function (ctgr_index, ctgr) {
                let colspan = Object.keys(ctgr.criteria).length;
                let category = ctgr.criterion_category;
                univ_th_ctgr += `<th class="comp__univ_table-category comp__univ_table-ctgr-${category.id}" colspan="${number_of_crtr}">${category.name}</th> `;
                let crtrs = ctgr.criteria;
                // $.each(crtrs, function(crtr_index, crtr){
                //     if(crtr_index <= number_of_crtr - 1){
                //         // univ_th_crtr += `<th class="comp__univ_table-criterion comp__univ_table-${category.id}-cr" criterion-id="${crtr.id}">${crtr.name}</th>`;
                //         // univ_th_sort += '<th>s</th>';
                //     }
                // });
            });
            $('#university_table_th-ctgr').html(univ_th_ctgr);
            // $('#university_table_th-crtr').html(univ_th_crtr);
            // $('#university_table_th-sort').html(univ_th_sort);

            callback();
        }
    });

    var subj_table_th = "";
    var subj_ctgrCrtr = [];
    var ctgr_with_criterions = [];
    var scores = [];
    var score_list = [];
    var crtr_width = 171;


    var groups_list;
    var univ_table_th = "";
    var univ_ctgrCrtr = [];

    jQuery(document).on('click touch', '.gs-btn', function () {
        let sectorName = $(this).text();
        iziToast.info({
            title: `Đã chọn khối ngành ${sectorName}!`,
            position: 'bottomLeft',
        });
        jQuery('.gs-btn').removeClass('btn-select');
        $('.gs-btn').find($('.fa')).removeClass('fa-check');
        jQuery(this).addClass('btn-select');
        $(this).find($('.fa')).addClass('fa-check');
        let sector_id = $(this).attr('id-gs');

        $('#ranking__subject_table-title').text('Xếp hạng ngành ' + sectorName);

        var subj_th_ctgr = '';
        var subj_expand = '';
        var subj_th_sort = '';
        subjTablData = [];
        widthArray = [];
        table_title_data(subj_ctgrCrtr, function () {
            get_subject_ranking();

        })

        function get_subject_ranking() {
            let url = `/api/v1/rank/sector`;
            let data = {
                sector: sector_id,
            }
            ajax_request(false, true, "GET", "json", url, null, data, subject_ranking_success_callback, error_callback);
        }

        $('.loader-img').fadeIn(200).delay(800).animate({
            height: "hide"
        }, 300);
        $('#ranking__subject-table').show();

        function table_title_data(array_of_ctgr, callback) {
            var containerWidth = $('.container').width();
            let univ_width = 200;
            let rank_width = 40;
            subj_th_ctgr = `<th class="bg-custom-2" rowspan="2" style="width:${rank_width}px">Thứ hạng</th>
                            <th class='rank__subj_table-category-h bg-custom-2' rowspan="2" style='width:${univ_width}px'>Trường</th>`;
            var ctgr_width = (containerWidth - univ_width - rank_width) / category_length;
            subj_th_sort = '<th> </th><th> </th>';
            $.each(array_of_ctgr, function (ctgr_index, ctgr) {
                let category = ctgr.criterion_category;
                subj_th_ctgr += `<th class="py-0 pr-0 ctgr comp__subj_table-category comp__subj_table-ctgr-${category.id}" category_id="${category.id}" style="width:${ctgr_width}px">${category.name}</th>`;
                subj_expand += `<th class="p-0"><btn class="btn p-3 w-100 change-crtr-btn" data-toggle="modal" data-target="#crtr-modal" ctgr-id="${category.id}" ctgr-name="${category.name}"><i>Xem thêm...</i></btn></th>`;
                subj_th_sort += '<th> </th>';
            });

            $('#subject_table_th-ctgr').html(subj_th_ctgr);
            $('#subject_expand_btn').html(subj_expand);
            $('#subject_table_th-sort').html(subj_th_sort);
            callback();
        }
        $($(this).attr('show')).animate({
            opacity: "show"
        }, 1000, function () {
            scroll_to_id($this);
        });

    });
    // var mdatatable_init = false;
    var category_table;
    var mtable_data = [];
    $(document).on('click touch', '.change-crtr-btn', function () {
        let id = $(this).attr('ctgr-id');
        let name = $(this).attr('ctgr-name');
        let crtrs = [];
        let criterion_th = '';
        let sort_th = '';
        let criterions_length = 0;
        let mData = [];
        mtable_data = [];
        $('.subject_rank_criterion').html('');
        $('.subject_rank_sort').html('');
        $('.modal-table-title').text(`Xếp hạng nhóm tiêu chí ${name}`);
        $(subj_ctgrCrtr).filter(function (_i, element) {
            if (element.criterion_category.id == id) {
                crtrs = element.criteria;
            }
        });
        criterions_length = crtrs.length;
        criterion_th += `<th class="univ-rank-th">Thứ hạng</th><th class='rank__univ_table-category' style="width:30%">Trường</th>`;
        sort_th += '<th></th><th></th>';
        mData.push({ "mData": 0 });
        mData.push({ "mData": 1 });
        
        $.each(crtrs, function (index, crtr) {
            criterion_th += `<th crtr-id="${crtr.id}">${crtr.name}</th>`;
            sort_th += '<th></th>';
            mData.push({"mData": index + 2 })
        });
        // console.log(mData);
        
        $('.subject_rank_criterion').html(criterion_th);
        $('.subject_rank_sort').html(sort_th);
        // if(mdatatable_init){
        //     category_table.destroy();
        
        // }
        // else {}
        // console.log(category_table);
        // let category_table = undefined;

        get_mdata(subject_rank_universities, id, criterions_length, function() {
            rank_by_category();
        });

        function get_mdata(university_list, id, criterions_length, callback) {
            university_list.forEach(function (university_obj, index) {
                let university = university_obj.profile.university;
                let general_statistics = university_obj.profile.general_statistics;
                let university_id = university.id;
                mtable_data[index] = new Array();
                mtable_data[index].push(`${general_statistics.rank}`, `${university.name}`); // += `<tr><td class="subj-rank">${general_statistics.rank}</td><td class="subj__table_univ-name">${university.name}</td>`;
                let scores = university_obj.scores;
                // console.log(scores);
                for (let i = 0; i < criterions_length; i++) {
                    let crtr_id = parseInt($(`.subject_rank_criterion th:nth-child(${i+3})`).attr('crtr-id'));
                    let score = "no data ...";
                    let ctgr_index = 0;
                    if (scores.length != 0) {
                        $(scores).filter(function(_i, param){
                            if(param.criterion_category_score.criterion_category.id == id) {
                                ctgr_index = scores.indexOf(param);
                            }
                        });
                        if(scores[ctgr_index] != undefined){
                            $(scores[ctgr_index].criterion_scores).filter(function(_i, param){
                                if(param.criterion.id == crtr_id){
                                    score = param.score;
                                    // console.log(score);
                                }
                            });
                        }
                    } else score = "no data ...";
                    mtable_data[index].push(`${score}`); //+= `<td class="comp__subj_table-${univ_id} comp__subj_table-cr-${crtr_id} comp__subj_score-ctgr-${ctgr_id}">${score}</td>`;
                }
            });
            callback();
        }

        function rank_by_category() {    
            if (category_table != undefined) {
                category_table.destroy();
                // alert("destroyed");
            }
            else {}
            // mdatatable_init = true;
            $('.rank-by-category-body').empty();
            
            category_table = $('.rank-by-category').DataTable({
                "language": {
                    "info": "Đang thể hiện từ trường số _START_ tới trường số _END_ trên tổng số _TOTAL_ trường",
                    "lengthMenu": "Số trường trên bảng: _MENU_ trường.",
                    "paginate": {
                        "next": "Trang sau",
                        "previous": "Trang trước",
                    },
                    "search": "Tìm kiếm: ",
                },
                "pageLength": 10,
                // "scrollY" : "200px",
                // "scrollColapse" : true,
                // "scrollX" : true,
                "data": mtable_data,
                "autoWidth": false, 
                "retrieve": true,
                // paging: false,
                // "destroy": true,
                "aoColumns": mData,
                
            });
        };
        
    });

    function error_callback(response) {
        alert("Đã xảy ra lỗi, xem response tại console");
    }

    var univ_for_test = [];

    function universities_ranking_success_callback(response) {
        university_rank_universities = response.rank;
        univTablData = [];
        widthArray = [];

        get_data(university_rank_universities, function () {
            display_data(function () {
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

        function get_data(arrays, callback) {
            arrays.forEach(function (univ, index) {
                let university = univ.profile.university;
                let general_statistics = univ.profile.general_statistics;
                let univ_id = university.id;
                univTablData[index] = new Array();
                univTablData[index].push(`${general_statistics.rank}`, `${university.name}`);
                let scores = univ.scores;

                for (let i = 0; i < 16; i++) {
                    let crtr_id = $(`#subject_table_th-crtr th:nth-child(${i+1})`).attr('crtr-id');
                    let ctgr_id = parseInt($(`#subject_table_th-crtr th:nth-child(${i+1})`).attr('ctgr-id'));
                    let ctgr_index = parseInt(i / 4);
                    let score = "n!"
                    if (scores.length != 0) {
                        $(scores[ctgr_index].criterion_scores).filter(function (_i, param) {
                            if (param.criterion.id == crtr_id) {
                                score = parseFloat(param.score);
                            }
                        });
                    } else score = "n!";
                    univTablData[index].push(`${score}`);
                }
            });
            callback();
        }

        function display_data(callback) {
            callback();
        }

        function width_setting() {
            widthArray[0] = $(`#subject_table_th-ctgr th:nth-child(1)`).width();
            widthArray[1] = $(`#subject_table_th-ctgr th:nth-child(2)`).width();
            for (let i = 1; i <= 16; i++) {
                widthArray[i + 1] = $(`#subject_table_th-crtr th:nth-child(${i})`).width();
            }

        }
    }



    var selected_univ = [];


    function get_all_sector() {
        let url = "/api/v1/sectors";
        ajax_request(false, true, "GET", "json", url, null, null, all_sectors_success_callback, error_callback);
    };
    // function get_criterion(category) {
    //     let url = `/api/v1/categories/${category}/criteria`;
    //     ajax_request(false, true, "GET", "json", url, null, null, criterion_success_callback, error_callback);        
    // };
    
    // function criterion_success_callback(response) {
    //     let criterions = response;

    // };
    
    
    function all_sectors_success_callback(response) {
        let sectors = response.sectors;
        let pane = "";
        $.each(sectors, function (index, sector) {
            pane += `<div class="col-md-6">
                        <btn class="btn gs-btn m-portlet py-3 my-1 w-100" id-gs="${sector.id}"><i class="fa mt-2" style="float:right"></i> ${sector.name}</btn>
                    </div>`;
        });
        $("#sector__area").html(pane);
        $("#sector__area").children().each(function () {
            $(this).addClass('animated fadeInDown');
        });

    }

    function get_all_category(target) {
        let url = "/api/v1/criteria";
        let data = {
            target: target,
        };
        if (target == "subject") {
            ajax_request(false, true, "GET", "json", url, null, null, all_category_subject_callback, error_callback);
        } else if (target == "university") {
            // data={};
            ajax_request(false, true, "GET", "json", url, null, null, all_category_university_callback, error_callback);
        }
    }

    function all_category_subject_callback(response) {
        let categories = response;
        category_length = categories.length;
        subj_ctgrCrtr = categories;

    }

    function all_category_university_callback(response) {
        univ_ctgrCrtr = response;
        category_length = categories.length;
    }

    var scores_index = 0;
    var table;

    function subject_ranking_success_callback(response) {
        subject_rank_universities = response.universities;

        subjTablData = [];
        widthArray = [];

        get_data(subject_rank_universities, function () {
            display_data(function () {
                width_setting();
                if (table != undefined) {
                    table.destroy();
                    // alert("destroyed");
                }
                table = $('.sort-table').DataTable({
                    // "searching": false,
                    // "lengthChange": false,
                    "language": {
                        "info": "Đang thể hiện từ trường số _START_ tới trường số _END_ trên tổng số _TOTAL_ trường",
                        "lengthMenu": "Số trường trên bảng: _MENU_ trường.",
                        "paginate": {
                            "next": "Trang sau",
                            "previous": "Trang trước",
                        },
                        "search": "Tìm kiếm: ",
                    },
                    "pageLength": 10,
                    // "scrollY" : "200px",
                    // "scrollColapse" : true,
                    // "scrollX" : true,
                    "data": subjTablData,
                    "autoWidth": true,

                    // drawCallback: function () { // this gets rid of duplicate headers
                    //     $('.dataTables_scrollBody thead tr').css({height:'0px'});
                    // },
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
                    //     exportOp     pplied'

                    // },
                    //     header: true,
                    //     footer: true,
                    // },
                    // ]
                });
                // $(".dataTables_scrollBody #subject_table_th-sort").empty();

            });
        });
        // function get_data(arrays, callback){
        //     arrays.forEach(function(univ, index){
        //         let university = univ.profile.university;
        //         let general_statistics = univ.profile.general_statistics;
        //         let univ_id = university.id;
        //         subjTablData[index] = new Array();
        //         subjTablData[index].push(`${general_statistics.rank}`, `${university.name}`);// += `<tr><td class="subj-rank">${general_statistics.rank}</td><td class="subj__table_univ-name">${university.name}</td>`;
        //         let scores = univ.scores;

        //         for(let i = 0; i < 20; i++){
        //             let crtr_id = $(`#subject_table_th-crtr th:nth-child(${i+1})`).attr('crtr-id');
        //             let ctgr_id = parseInt($(`#subject_table_th-crtr th:nth-child(${i+1})`).attr('ctgr-id'));
        //             let ctgr_index = parseInt(i/4);
        //             let score = "n!";
        //             if(scores.length != 0){

        //                 if(scores[ctgr_index] != undefined){

        //                     $(scores[ctgr_index].criterion_scores).filter(function(_i, param){
        //                         if(param.criterion.id == crtr_id){
        //                             score = param.score;
        //                             console.log(score);
        //                         }
        //                     });
        //                 }
        //             }
        //             else score = "n!";
        //             subjTablData[index].push(`${score}`); //+= `<td class="comp__subj_table-${univ_id} comp__subj_table-cr-${crtr_id} comp__subj_score-ctgr-${ctgr_id}">${score}</td>`;
        //         }
        //         // subjTablData += '</tr>';
        //     });
        //     callback();
        // }
        function get_data(arrays, callback) {
            arrays.forEach(function (univ, index) {
                let university = univ.profile.university;
                let general_statistics = univ.profile.general_statistics;
                let univ_id = university.id;
                subjTablData[index] = new Array();
                subjTablData[index].push(`${general_statistics.rank}`, `${university.name}`); // += `<tr><td class="subj-rank">${general_statistics.rank}</td><td class="subj__table_univ-name">${university.name}</td>`;
                let scores = univ.scores;
                for (let i = 0; i < category_length; i++) {
                    let ctgr_id = parseInt($(`#subject_table_th-ctgr th:nth-child(${i+3})`).attr('category_id'));
                    let score = "Chưa có dữ liệu...";
                    if (scores.length != 0) {
                        $(scores).filter(function (_i, param) {
                            if (param.criterion_category_score.criterion_category.id == ctgr_id) {
                                score = parseFloat(param.criterion_category_score.score);
                            }
                        });
                    } else score = "Chưa có dữ liệu...";
                    subjTablData[index].push(`${score}`); //+= `<td class="comp__subj_table-${univ_id} comp__subj_table-cr-${crtr_id} comp__subj_score-ctgr-${ctgr_id}">${score}</td>`;
                }
                // subjTablData += '</tr>';
            });
            callback();
        }

        function display_data(callback) {
            callback();
        }

        function width_setting() {
            // widthArray[0] = $(`#subject_table_th-ctgr th:nth-child(1)`).width();
            // widthArray[1] = $(`#subject_table_th-ctgr th:nth-child(2)`).width();
            // for(let i = 1; i <= 16; i++){
            //     widthArray[i+1] = $(`#subject_table_th-crtr th:nth-child(${i})`).width();
            // }

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
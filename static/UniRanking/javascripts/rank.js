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
    var subjTablData = new Array();
    var univTablData = new Array();
    var widthArray = new Array();
    var univ_table_body = '';
    var univ_table_th = "";
    var univ_ctgrCrtr = [];


    $('#navibar').addClass('navbar__over');
    iziToast.settings({
        timeout: 2500,
    });

    get_all_sector();
    get_all_category();
    

    $(document).on('click touch', '#university-rank-btn', function () {
        // iziToast.info({
        //     title: 'Đã chọn xếp hạng theo trường!',
        //     position: 'bottomLeft',
        // });
        var univ_th_ctgr = '';
        var univ_th_crtr;
        var univ_expand = '';
        var univ_th_sort;
        


        $('.gs-btn').removeClass('btn-select');
        $('.gs-btn').find($('.fa')).removeClass('fa-check');
        $(this).find($('.fa')).removeClass('fa-check');        
        $(this).addClass('btn-select');
        $(this).find($('.fa')).addClass('fa-check');
        // alert(univ_ctgrCrtr);
        set_table_title_data(univ_ctgrCrtr, function() {
            get_university_rank();
        });
            
        function get_university_rank() {
            let url = '/api/v1/rank/university';
            ajax_request(false, true, "GET", "json", url, null, null, university_rank_success_callback, error_callback);            
        };

        

        $('.loader-img').fadeIn(200).delay(800).animate({
            height: "hide"
        }, 300);
        $('#ranking__subject-table').hide();
        $('#ranking__university-table').show();
        
        

        function set_table_title_data(array_of_ctgr, callback) {
            var containerWidth = $('.container').width();
            let univ_width = 200;
            let rank_width = 40;
            univ_th_ctgr = `<th class="bg-custom-2" rowspan="2" style="width:${rank_width}px">Thứ hạng</th>
                            <th class='rank__univ_table-category-h bg-custom-2' rowspan="2" style='width:${univ_width}px'>Trường</th>`;
            var ctgr_width = (containerWidth - univ_width - rank_width) / category_length;
            univ_th_sort = '<th> </th><th> </th>';
            $.each(array_of_ctgr, function (ctgr_index, ctgr) {
                let category = ctgr.criterion_category;
                univ_th_ctgr += `<th class="p-2 ctgr comp__subj_table-category comp__subj_table-ctgr-${category.id}" category_id="${category.id}" style="width:${ctgr_width}px">${category.name}</th>`;
                univ_expand += `<th class="p-0"><btn class="btn p-3 w-100 u-expand-btn" data-toggle="modal" data-target="#crtr-modal" ctgr-id="${category.id}" ctgr-name="${category.name}"><i>Xem thêm...</i></btn></th>`;
                univ_th_sort += '<th> </th>';
            });
            $('#university_table_th-ctgr').html(univ_th_ctgr);
            $('#university_expand_btn').html(univ_expand);
            $('#university_table_th-sort').html(univ_th_sort);
            callback();
        };
        $($(this).attr('show')).animate({
            opacity: "show"
        }, 1000, function () {
            scroll_to_id($this);
        });
    });

    var subj_table_th = "";
    var subj_ctgrCrtr = [];
    var ctgr_with_criterions = [];
    var scores = [];
    var score_list = [];
    var crtr_width = 171;
    

    var groups_list;
    
    $(document).on('click touch', '.gs-btn', function () {
        let sectorName = $(this).text();
        iziToast.info({
            title: `Đã chọn khối ngành ${sectorName}!`,
            position: 'bottomLeft',
        });
        $('.gs-btn').removeClass('btn-select');
        $('#university-rank-btn').removeClass('btn-select');
        $("#university-rank-btn").find($('.fa')).removeClass('fa-check');        
        
        $('.gs-btn').find($('.fa')).removeClass('fa-check');
        $(this).addClass('btn-select');
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
        $('#ranking__university-table').hide();
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
                subj_th_ctgr += `<th class="p-0 ctgr comp__subj_table-category comp__subj_table-ctgr-${category.id}" category_id="${category.id}" style="width:${ctgr_width}px">${category.name}</th>`;
                subj_expand += `<th class="p-0"><btn class="btn p-3 w-100 s-expand-btn" data-toggle="modal" data-target="#crtr-modal" ctgr-id="${category.id}" ctgr-name="${category.name}"><i>Xem thêm...</i></btn></th>`;
                subj_th_sort += '<th> </th>';
            });
            
            $('#subject_table_th-ctgr').html(subj_th_ctgr);
            $('#subject_expand_btn').html(subj_expand);
            $('#subject_table_th-sort').html(subj_th_sort);
            callback();
        };
        $($(this).attr('show')).animate({
            opacity: "show"
        }, 1000, function () {
            scroll_to_id($this);
        });

    });
    // var mdatatable_init = false;
    var category_table;
    var mtable_data = [];
    $(document).on('click touch', '.s-expand-btn', function () {
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

    //University modal table

    $(document).on('click touch', '.u-expand-btn', function () {
        let id = $(this).attr('ctgr-id');
        let name = $(this).attr('ctgr-name');
        let crtrs = [];
        let criterion_th = '';
        let sort_th = '';
        let criterions_length = 0;
        let mData = [];
        mtable_data = [];
        $('.university_rank_criterion').html('');
        $('.university_rank_sort').html('');
        $('.modal-table-title').text(`Xếp hạng nhóm tiêu chí ${name}`);
        $(univ_ctgrCrtr).filter(function (_i, element) {
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

        get_mdata(university_rank_universities, id, criterions_length, function() {
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

    var selected_univ = [];


    function get_all_sector() {
        let url = "/api/v1/sectors";
        ajax_request(false, true, "GET", "json", url, null, null, all_sectors_success_callback, error_callback);
    };
    
    
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

    function get_all_category() {
        let url = "/api/v1/criteria";
        ajax_request(false, true, "GET", "json", url, null, null, all_category_success_callback, error_callback);    
    }

    function all_category_success_callback(response) {
        let categories = response;
        category_length = categories.length;
        subj_ctgrCrtr = categories;
        univ_ctgrCrtr = categories;
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
                }
                table = $('#subject-table').DataTable({
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
                    "data": subjTablData,
                    "autoWidth": true,
                });
                
            });
        });
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
                    subjTablData[index].push(`${score}`);
                }
            });
            callback();
        }

        function display_data(callback) {
            callback();
        }

        function width_setting() {
        }
    }
    
    //University Rank
    function university_rank_success_callback(response) {
        university_rank_universities = response.rank;
        univTablData = [];
        widthArray = [];
        
        get_data(university_rank_universities, function() {
            // width_setting();
            if (table != undefined) {
                table.destroy();
            }
            table = $('#university-table').DataTable({
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
                "data": univTablData,
                // "autoWidth": true,
            });
        });

        function get_data(arrays, callback) {
            arrays.forEach(function (univ, index) {
                let university = univ.profile.university;
                let general_statistics = univ.profile.general_statistics;
                let univ_id = university.id;
                univTablData[index] = new Array();
                univTablData[index].push(`${general_statistics.rank}`, `${university.name}`); // += `<tr><td class="subj-rank">${general_statistics.rank}</td><td class="subj__table_univ-name">${university.name}</td>`;
                let scores = univ.scores;
                for (let i = 0; i < category_length; i++) {
                    let ctgr_id = parseInt($(`#university_table_th-ctgr th:nth-child(${i+3})`).attr('category_id'));
                    let score = "Chưa có dữ liệu...";
                    if (scores.length != 0) {
                        $(scores).filter(function (_i, param) {
                            if (param.criterion_category_score.criterion_category.id == ctgr_id) {
                                score = parseFloat(param.criterion_category_score.score);
                            }
                        });
                    } else score = "Chưa có dữ liệu...";
                    univTablData[index].push(`${score}`);
                }
            });
            callback();
        }
        function width_setting() {
        }
    };
});
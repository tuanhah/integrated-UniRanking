function update_subject_list(){
    let csrftoken = getCookie('csrftoken');
    let url = "/api/subjects";
    univ_id = $("#subject_list").data("university-id");
    let data = {
        csrfmiddlewaretoken: csrftoken,
        university: univ_id
    };
    ajax_request(data, "POST", "json", url, subjects_success_callback, error_callback);
}

function update_scores_list(subj_id = undefined){
    let csrftoken = getCookie('csrftoken');
    let url = "/api/scores";
    univ_id = $("#subject_list").data("university-id");
    let data = {
        csrfmiddlewaretoken: csrftoken,
        university: univ_id,
    };
    if (subj_id !== undefined) {
        data.subject = subj_id;
    }
    ajax_request(data, "POST", "json", url, scores_get_success_callback, error_callback);
}

function update_group_choices(sector_id){
    let csrftoken = getCookie('csrftoken');
    let url = "/api/groups";
    let data = {
        csrfmiddlewaretoken: csrftoken,
        sector : sector_id,
    };
    ajax_request(data, "POST", "json", url, group_choices_success_callback, error_callback);
}

function update_subject_choices(university_id, group_id){
    let csrftoken = getCookie('csrftoken');
    let url = "/api/editor/subjects";
    let data = {
        csrfmiddlewaretoken: csrftoken,
        university : university_id,
        group : group_id,
    };
    ajax_request(data, "POST", "json", url, subject_choices_success_callback, error_callback);
}

function edit_score(university, subject, criterion, score, success_callback){
    let csrftoken = getCookie('csrftoken');
    let url = "/api/editor/scores/edit";
    let target = (subject != undefined) ? "subject" : "university"
    let data = {
        csrfmiddlewaretoken: csrftoken,
        target : target,
        university : university,
        subject : subject,
        criterion : criterion,
        score : score
    };
    ajax_request(data, "POST", "json", url, success_callback, error_callback);
}

function delete_score(university, subject, criterion, success_callback){
    let csrftoken = getCookie('csrftoken');
    let url = "/api/editor/scores/delete";
    let data = {
        csrfmiddlewaretoken: csrftoken,
        university : university,
        subject : subject,
        criterion : criterion,
    };
    ajax_request(data, "POST", "json", url, success_callback, error_callback);
}

function update_criterion_score_modal(university, subject, category){
    let csrftoken = getCookie('csrftoken');
    let url = "/api/editor/criteria";
    let target = (subject != undefined) ? "subject" : "university"
    let data = {
        csrfmiddlewaretoken: csrftoken,
        target : target,
        university : university,
        subject : subject,
        category : category,
    };
    ajax_request(data, "POST", "json", url, criterion_choices_success_callback, error_callback);
}

function update_category_criterion_choices(target){
    let csrftoken = getCookie('csrftoken');
    let url = "/api/editor/criteria/categories";
    let data = {
        csrfmiddlewaretoken: csrftoken,
        target : target
    };
    ajax_request(data, "POST", "json", url, criterion_category_choices_success_callback, error_callback);
}

function criterion_category_choices_success_callback(response){
    if(response.success){
        let categories = response.categories;
        let html = '<option value="0">------- Chọn nhóm tiêu chí------</option>'
        $.each(categories, function(index, category){
            html += `<option value="${category.id}">${category.name}</option>`
        });
        $("#category_list_select").html(html);
    }
}

function criterion_choices_success_callback(response){
    if(response.success){
        let added_criterion_scores = response.added_criterion_scores;
        let non_added_criterion_scores = response.non_added_criterion_scores;
        (function(){
            let html_non_added_cri = '<option value="0">------- Chọn tiêu chí -------</option>';
            $.each(non_added_criterion_scores, function(index, criterion_score){
                html_non_added_cri += `<option value="${criterion_score.id}">${criterion_score.name}</option>`
            });
            $("#criterion_list_select").html(html_non_added_cri);
        })();

        (function(){
            let html_added_cri = "";
            $.each(added_criterion_scores, function(index, criterion_score){
                html_added_cri += `<tr>
                <td class="criterion_name" data-criterion-id="${criterion_score.id}">${criterion_score.name}</td>
                <td class="text-center">${criterion_score.score}</td>
                <td class="text-center">
                    <button class="btn btn-outline-secondary border-0 score_delete_confirm"><i class="fas fa-minus"></i></button>
                </td>
            </tr>`
            });
            $("#added_score_field").html(html_added_cri);
        })();
        
    }
}

function subject_choices_success_callback(response){
    if(response.success){
        subjects = response.subjects;
        let html = "";
        $.each(subjects, function(index, subject){
            let html_subject_toggle = ""
            if(subject.added){
                html_subject_toggle = '<button class="btn btn-outline-secondary border-0 subject_delete_button"><i class="fas fa-minus"></i></button>'
            }else{
                html_subject_toggle = '<button class="btn btn-outline-success border-0 subject_add_button"><i class="fas fa-plus"></i></button>'
            }
            html += `<a class="list-group-item list-group-item-action" data-subject-id="${subject.id}">${subject.name} ${html_subject_toggle}</a>`
        });
        let subject_list_select_dom = $("#subject_list_select");
        subject_list_select_dom.html(html);
        subject_list_select_dom.parent().slideDown();
        subject_list_select_dom.animate({ scrollTop: 0 }, "fast");
    }
}

function group_choices_success_callback(response){
    if(response.success){
        let groups = response.groups
        let html = '<option value="0">-------- Chọn nhóm ngành --------</option>'
        $.each(groups, function(index, group){
            html += `<option value="${group.id}">${group.name}</option>`
        });
        $("#subject_group_select").html(html);
    }
}

function subjects_success_callback(response) {
    let univ_name = response.name;
    let html_subject_delete = ""
    let html_subject_add = ""
    if (response.editable) {
        html_subject_delete = '<i class="far fa-trash-alt subject_delete_button"></i>';
        html_subject_add = '<i id="subject_add" class="fas fa-plus-circle fa-lg" data-toggle="modal" data-target="#add_subject_modal"></i>';
    }
    let editable = response.editable;
    let subjects = response.subjects;
    let html = `<a class="uni_whole" id="active_subject">Toàn Trường ${html_subject_add}</a>`;
    $.each(subjects, function (root_group, groups) {
        html += `<div class="dropdown_list">
                    <a class="dropdown_toggle"> ${root_group}</a>
                    <div class="dropdown_content">`
        $.each(groups, function (group, subjects) {
            html += `<div class="dropdown_list">
                        <a class="dropdown_toggle">${group}</a>
                        <div class="dropdown_content">`
            $.each(subjects, function (subj_name, subj_id) {
                html += `<a class="subject" data-subject-id ="${subj_id}">${subj_name} ${html_subject_delete}</a>`
            });
            html += `</div>
                </div>`
        });
        html += `</div>
            </div>`
    });
    $("#subject_list").html(html);
    
    (function(){
        update_scores_list();        
    })();
}

function scores_get_success_callback(response) {
    let title_color = ["#6F3A00", "#008A5B", "#6B3650", "#E59C23", "#9474B0"]
    let table_body = $("#score_table tbody").empty();
    let subject_name = response.name;
    let scores = response.scores;
    $("#score_title").text(subject_name);
    if ($.isEmptyObject(scores)) {
        table_body.append(`<div class="alert alert-warning mt-4" role="alert">
                            Đang cập nhật, vui lòng quay lại sau
                            </div>`)
    }
    $.each(scores, function (category_cri, data) {
        color = title_color.pop();
        let header = `<tr class="category_score" style="background-color: ${color};" >
                    <td class="category_name" data-category-criterion-id="${data.id}">${category_cri}</td>
                    <td class="score_cell text-center">
                        ${data.score}
                    </td>
                </tr>`;
        let body = "";
        $.each(data.detail, function (index, detail) {
            body += `<tr class="criterion_score">
                        <td class="criterion_name" data-criterion-id="${detail.id}">${detail.name}</td>
                        <td class="text-center score_cell">
                                <div class="score_base">
                                    ${detail.score}
                                </div>
                                <div class="score_edit_button" style="display:none;">
                                    <i class="fas fa-edit fa-lg"></i>
                                </div>
                        </td>
                    </tr>`;
        });
        table_body.append(header + body);
    });
}

function delete_subject_success_callback(response) {
    if (response.success) {
        subject = response.subject;
        alert(`Đã xóa ngành ${subject}`)
        update_subject_list()
    }
}

function error_callback(response) {
    console.log(response)
    alert("Có lỗi trong quá trình lấy dữ liệu.")
}

$(document).ready(function () {
    $("body").on("click", ".dropdown_toggle", function (e) {
        let dropdown_content = $(this).parent().children(".dropdown_content");
        dropdown_content.slideToggle();
    });

    $("body").on("click", ".subject, .uni_whole", function (e) {
        $("#active_subject").removeAttr("id");
        $(this).attr("id", "active_subject");
        subj_id = $(this).data("subject-id");
        update_scores_list(subj_id);
    });

    $("body").on("click", ".subject_delete_button", function (e) {
        e.stopPropagation();
        let that = this
        let csrftoken = getCookie('csrftoken');
        let url = "/api/editor/subjects/delete";
        univ_id = $("#subject_list").data("university-id");
        subj_id = $(this).parent().data("subject-id");
        let data = {
            csrfmiddlewaretoken: csrftoken,
            university: univ_id,
            subject: subj_id
        };
        let success_callback = undefined;
        add_subject_modal_dom = $(this).parents("#add_subject_modal")
        if(add_subject_modal_dom.length >= 1){ // deleting subject from modal
            success_callback = function(response){
                if(response.success){
                    $(that).removeClass("btn-outline-secondary subject_delete_button").addClass("btn-outline-success subject_add_button");   
                    $(that).html('<i class="fas fa-plus">');
                }
            }
        }else{
            success_callback = delete_subject_success_callback;
        }
        ajax_request(data, "POST", "json", url, success_callback, error_callback);
    });

    $("body").on("click", ".subject_add_button", function (e) {
        e.stopPropagation();
        let that = this
        let csrftoken = getCookie('csrftoken');
        let url = "/api/editor/subjects/add";
        univ_id = $("#subject_list").data("university-id");
        subj_id = $(this).parent().data("subject-id");
        let data = {
            csrfmiddlewaretoken: csrftoken,
            university: univ_id,
            subject: subj_id
        };
        ajax_request(data, "POST", "json", url, function(response){
            if(response.success){
                $(that).removeClass("btn-outline-success subject_add_button").addClass("btn-outline-secondary subject_delete_button");
                $(that).html('<i class="fas fa-minus">');
            }
        }, error_callback);
    });

    $("#subject_sector_select").on("change", function(e){
        let sector_id = $(this).val();
        if(sector_id > 0){
            update_group_choices(sector_id);
        }else{
            $("#subject_group_select").empty();
        }
        $("#subject_list_select").empty().parent().slideUp();
    });

    $("#subject_group_select").on("change", function(e){
        let group_id = $(this).val();
        if(group_id > 0){
            univ_id = $("#subject_list").data("university-id");
            update_subject_choices(univ_id, group_id);
        }else{
            $("#subject_list_select").empty().parent().slideUp();
        }
    });

    $("#add_subject_modal").on("hide.bs.modal", function(e){
        $("#subject_sector_select").val(0).trigger("change");
        update_subject_list()
    });

    $("#score_table").on("mouseenter mouseleave", ".score_cell", function(e){
        if( $(this).find("input").length == 0){
            if(e.type == "mouseenter"){
                $(this).children(".score_base").stop().fadeOut('fast',function(){
                    $(this).siblings().stop().fadeIn('fast');  
                });    
            }else{
                $(this).children(".score_edit_button").stop().fadeOut('fast', function(){
                    $(this).siblings().stop().fadeIn('fast');  
                });    
            }
        }
    });

    $("#score_table").on("click", ".criterion_score .score_edit_button", function(e){
        if( $(this).children().is("i")){
            let score = $(this).siblings().text();
            let html_input = `<div class="row position-relative">
                                <div class="col-5 mx-auto">
                                    <input type="text" class="form-control text-center" value=${score}>
                                </div>
                                <div class="edit_choice">
                                    <i class="fas fa-check fa-lg edit_score_confirm"> </i> 
                                    <i class="fas fa-times fa-lg edit_score_cancel"></i>
                                </div>
                            </div>`
            $(this).html(html_input).children("input").focus();
        }
    });

    $("#score_table").on("click", ".criterion_score .edit_score_confirm", function(e){
        let row_dom = $(this).closest(".criterion_score");
        let new_score = row_dom.find("input").val();
        let cri_id = row_dom.find(".criterion_name").data("criterion-id");
        let univ_id = $("#subject_list").data("university-id");
        let active_subject_dom =  $("#active_subject");
        let subj_id = undefined;
        if(!active_subject_dom.hasClass("uni_whole")){
            subj_id = active_subject_dom.data("subject-id");
        }
        let callback = function(response){
            if(response.success){
                let score_cell_dom = row_dom.find(".score_cell");
                score_cell_dom.children(".score_base").text(score);
                let html_edit_button = '<i class="fas fa-edit fa-lg"></i>';
                score_cell_dom.children(".score_edit_button").html(html_edit_button);
            }
        };

        edit_score(university = univ_id, subject = subj_id, criterion = cri_id, score = new_score, success_callback = callback);
    });

    $("#score_table").on("click", ".criterion_score .edit_score_cancel", function(e){
        let score_edit_button_dom = $(this).closest(".score_edit_button");
        let html_edit_button = '<i class="fas fa-edit fa-lg"></i>';
        score_edit_button_dom.html(html_edit_button);
    });

    $("#score_add").on("click", function(e){
        let active_subject_dom =  $("#active_subject");
        let target = "";
        if(!active_subject_dom.hasClass("uni_whole")){
            target = "subject";
        }else{
            target = "university"
        }
        update_category_criterion_choices(target);
        $("#add_score_modal").modal("show");
        $("#category_list_select").focus();
    });

    $("#add_score_modal").on("hide.bs.modal",function(){
        $("#category_list_select").val(0).trigger("change");
        let subj_id = undefined;
        let active_subject_dom =  $("#active_subject");
        if(!active_subject_dom.hasClass("uni_whole")){
            subj_id = active_subject_dom.data("subject-id");
        }
        update_scores_list(subj_id);        
    });
    
    $("#category_list_select").on("change", function(e){
        let univ_id = $("#subject_list").data("university-id");
        let active_subject_dom =  $("#active_subject");
        let subj_id = undefined;
        if(!active_subject_dom.hasClass("uni_whole")){
            subj_id = active_subject_dom.data("subject-id");
        }
        let category_id = $(this).val();
        if(category_id > 0){
            update_criterion_score_modal(univ_id, subj_id, category_id);
        }else{
            $("#criterion_list_select").empty().trigger("change");
            $("#score_input").val("");
            $("#added_score_field").empty();
        }
    });

    $("#score_add_confirm").on("click", function(e){
        let row_dom = $(this).closest("tr");
        let cri_id = row_dom.find("#criterion_list_select").val();
        let cri_name = row_dom.find("#criterion_list_select option:selected").text();
        let score = row_dom.find("#score_input").val();
        let univ_id = $("#subject_list").data("university-id");
        let active_subject_dom =  $("#active_subject");
        let subj_id = undefined;
        if(!active_subject_dom.hasClass("uni_whole")){
            subj_id = active_subject_dom.data("subject-id");
        }

        let callback = function(response){
            if(response.success){
                $("#criterion_list_select").find(":selected").remove().end().val(0).trigger("change");
                $("#added_score_field").append(
                `<tr>
                    <td class="criterion_name" data-criterion-id="${cri_id}">${cri_name}</td>
                    <td class="text-center">${score}</td>
                    <td class="text-center">
                        <button class="btn btn-outline-secondary border-0 score_delete_confirm"><i class="fas fa-minus"></i></button>
                    </td>
                </tr>`);
            }else{
                if(response.score){
                    let error = response.score[0];
                    $("#score_input").addClass("is-invalid");
                    alert(error.message);
                }
            }
        };

        edit_score(university = univ_id, subject = subj_id, criterion = cri_id, score = score, success_callback = callback);
    });

    $("#added_score_field").on("click", ".score_delete_confirm", function(){
        let row_dom = $(this).closest("tr");
        let criterion_dom = row_dom.find(".criterion_name");
        let cri_id = criterion_dom.data("criterion-id");
        let cri_name = criterion_dom.text();
        let univ_id = $("#subject_list").data("university-id");
        let active_subject_dom =  $("#active_subject");
        let subj_id = undefined;
        if(!active_subject_dom.hasClass("uni_whole")){
            subj_id = active_subject_dom.data("subject-id");
        }

        let callback = function(response){
            if(response.success){
                row_dom.remove();
                $("#criterion_list_select").append(`<option value=${cri_id}>${cri_name}</option>`);
            }
        };
        delete_score(university = univ_id, subject = subj_id, criterion = cri_id, success_callback = callback);
    })

    $("#criterion_list_select").on("change", function(e){
        $("#score_input").removeClass("is-invalid").val("");
    });

    (function () {
        update_subject_list();
    })();
});
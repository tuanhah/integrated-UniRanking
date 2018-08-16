$(document).ready(function () {
    var logined = $('#user-authenticated').attr('logined');
    var current_user = $('#user-menu').attr('user-id');
    var id = $('#uni-name').attr('university_id');
    $('#navibar').addClass('navbar__over');
    university_scores(id);

    if (logined == 'true') {
        get_favourite_universities(current_user);
    }

    $(document).on('click', '#add-funiv', function () {
        if (logined == 'true') {
            add_favourite_university(current_user, id);
        }
        else {
            toastr.warning(`Bạn cần đăng nhập để thực hiện chức năng này`);
        }
    });
    
    $(document).on('click', '#remove-funiv', function () {
        remove_favourite_university(current_user, id);
    })


});

function university_scores(university) {
    let url = `/api/v1/universities/${university}/scores`;
    ajax_request(false, true, "GET", "json", url, null, null, university_scores_success_callback, error_callback);
}

function university_scores_success_callback(response) {
    let university = response;
    let scores = university.scores;
    let accordion_content = '';
    if (university.scores.length == 0) {
        accordion_content = '<div class="alert alert-warning w-100">Trường này chưa có điểm! Bạn vui lòng quay lại sau ...</div>'
    };
    $.each(scores, function (index, score) {
        let category_id = score.criterion_category_score.criterion_category.id;
        let category_name = score.criterion_category_score.criterion_category.name;
        let category_score = score.criterion_category_score.score;
        let criterions = score.criterion_scores;
        accordion_content += `<div class="m-accordion__item">
        <div class="m-accordion__item-head collapsed" role="tab" id="category-${category_id}-btn" data-toggle="collapse" href="#category-${category_id}" aria-expanded="false">
            <span class="m-accordion__item-icon">
                <i class="la la-angle-double-right"></i>
            </span>
            <span class="m-accordion__item-title">${category_name}</span>
            <span class="m-accordion__item-mode"></span>
        </div>
        <div class="m-accordion__item-body collapse" id="category-${category_id}" role="tabpanel" aria-labelledby="category-${category_id}-btn" data-parent="#university-score-accordion">
            <div class="m-accordion__item-content">
                <p><strong class="m--pull-right">${category_score}</strong> <strong>Điểm nhóm tiêu chí:</strong></p>
                <div class="m-separator m-separator--brand"></div>`;
        $.each(criterions, function (_index, criterion) {
            let criterion_name = criterion.criterion.name;
            let criterion_score = criterion.score;
            accordion_content += `<p><i class="m--pull-right">${criterion_score}</i>${criterion_name}</p>
            <div class="m-separator m-separator--dashed"></div>`;
        });
        accordion_content += '</div></div></div>';
    });
    $('#university-score-accordion').html(accordion_content);
}

function get_favourite_universities(user_id) {
    let url = `/api/v1/user/favourite?user=${user_id}`;
    ajax_request(false, true, "GET", "json", url, null, null, check_favourite_universities_success_callback, error_callback);
}

function check_favourite_universities_success_callback(response) {
    let favourite_universities = response.favourite_universities;
    let favourite_uid = [];
    let uid = $('#uni-name').attr('university_id');

    favourite_universities.forEach(function (university) {
        favourite_uid.push(university.university.id);
    });
    if (favourite_uid.indexOf(parseInt(uid)) != -1) {
        $('#favourite-btn').html('<i class="col-1 la la-heart pointer-md-icon" data-toggle="tooltip" title="Bạn đã yêu thích trường này" id="remove-funiv"></i>');
    }
    else $('#favourite-btn').html('<i class="col-1 la la-heart-o pointer-md-icon" data-toggle="tooltip" title="Thêm vào danh sách yêu thích" id="add-funiv"></i>');
}

function add_favourite_university(user, university) {
    let csrftoken = getCookie("csrftoken");
    let url = '/api/v1/edit/favourite/add_university';
    data = [{
        name: "university",
        value: university
    }];
    data.push({
        name: "csrfmiddlewaretoken",
        value: csrftoken
    });
    ajax_request(false, true, "POST", "json", url, null, data, add_favourite_universities_success_callback, error_callback);
}

function add_favourite_universities_success_callback(response) {
    let result = response;
    if (result.success === true) {
        toastr.success(`Bạn đã thêm thành công trường "${result.name}" vào danh sách yêu thích`);
    }
    else {
        let error = '';
        error = "Không thể thêm trường này. Bạn hãy kiểm tra lại !";
        toastr.error(error);
    }
    let current_user = $('#user-menu').attr('user-id');

    get_favourite_universities(current_user);
    // setTimeout(function () {
    //     window.location.reload()
    // }, 3000);
}

function remove_favourite_university(user, university) {
    let csrftoken = getCookie("csrftoken");
    let url = '/api/v1/edit/favourite/remove_university';
    data = [{
        name: "university",
        value: university
    }];
    data.push({
        name: "csrfmiddlewaretoken",
        value: csrftoken
    });
    ajax_request(false, true, "POST", "json", url, null, data, remove_favourite_universities_success_callback, error_callback);
}

function remove_favourite_universities_success_callback(response) {
    let result = response;
    if (result.success === true) {
        toastr.info(`Bạn đã xoá thành công trường "${result.name}" khỏi danh sách yêu thích`);
    }
    else {
        let error = '';
        error = "Không thể xóa trường này. Bạn hãy kiểm tra lại !";
        toastr.error(error);
    }
    let current_user = $('#user-menu').attr('user-id');

    get_favourite_universities(current_user);

}

function error_callback(response) {
    console.log(response)
    alert("Có lỗi trong quá trình lấy dữ liệu.")
};
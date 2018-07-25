// var scores;

$(document).ready(function () {
    $('#navibar').addClass('navbar__over');
    var id = $('#uni-name').attr('university_id');
    university_scores(id);


});

function university_scores(university) {
    let url = `/api/v1/universities/${university}/scores`;
    ajax_request(false, true, "GET", "json", url, null, null, university_scores_success_callback, error_callback);
}

function university_scores_success_callback(response) {
    university = response;
    // console.log(university.scores[0]);
    let scores = university.scores;
    let accordion_content = '';
    if(university.scores.length == 0) {
        accordion_content = '<div class="alert alert-warning w-100">Trường này chưa có điểm! Bạn vui lòng quay lại sau ...</div>'
    }
    
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

function error_callback(response) {
    console.log(response)
    alert("Có lỗi trong quá trình lấy dữ liệu.")
};
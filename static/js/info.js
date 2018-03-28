// jQuery('.info-multiple-select').select2({ maximumSelectionLength:1});
    
jQuery(document).ready(function(){
        jQuery('.info-multiple-select').select2({
            maximumSelectionLength: 1
        });
        get_university_list();
        jQuery('#uni-info-btn').click(function() {
            var uniName = jQuery('.info-multiple-select').find('option:selected').attr('u-name');
            jQuery('#uni-name').text(uniName);
            $('#all-info').show();  
        })
        // {% for cacr in CategoryCriterion %}
        // jQuery('#info-category-criterion-{{ cacr.id }}').click(function(){
        //     jQuery('#score-{{ cacr.id }}').toggleClass('show');
        // });
        // {% endfor %}
        // {% for cr in Criterion %}
        // jQuery('#score-cr-{{ cr.id }}-btn').click(function(){
        //     jQuery('.row-cr').hide();
        //     jQuery('#row-cr-{{ cr.id }}').show();
        // });

        // {% endfor %}
        jQuery('.btn-2').click(function(){
            jQuery('.btn-2').removeClass("btn-select");
            jQuery(this).addClass('btn-select');
        });
        jQuery('#show-all-score').click(function(){
            jQuery('.row-cr').show();
        });
    });
function error_callback(response) {
    console.log(response)
    alert("Có lỗi trong quá trình lấy dữ liệu.")
}
function get_university_list(){
    let csrftoken = getCookie('csrftoken');
    let url = "/api/universities";
    let data = {
        csrfmiddlewaretoken: csrftoken,
        
    };
    ajax_request(data, "POST", "json", url, university_success_callback, error_callback);
}

function university_success_callback(response){
    if(response.success){
        let universities = response.universities;
        // alert(university);
        let html = ''
        $.each(universities, function(index, uni){
            html += `<option value="${uni.id}" u-name="${uni.name}" >${uni.name}</option>`
        });

        $("#university-list").html(html);
    }
};


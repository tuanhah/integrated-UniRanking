function success_callback(response){
    let title_color = ["#6F3A00", "#008A5B", "#6B3650", "#E59C23", "#9474B0"]
    if(response.success){
        let table_body = $("#score_table tbody").empty();
        delete response["success"];
        if ($.isEmptyObject(response)){
            table_body.append(`<div class="alert alert-warning mt-4" role="alert">
                                Đang cập nhật, vui lòng quay lại sau
                                </div>`)
        }
        $.each(response,function(key, data){
            color = title_color.pop();
            let header = `<tr class="category_score" style="background-color: ${color};" >
                        <td>${key}</td>
                        <td class="text-center">${data.score}
                    </tr>`;
            let body = "";
            $.each(data.detail,function(key,detail){
                body += `<tr class="criterion_score">
                            <td>${detail.name}</td>
                            <td class="text-center">${detail.score}</td>
                        </tr>`;
            });
            table_body.append(header + body);
        });   
    }
}

function error_callback(response){
    console.log(response)
    alert("Có lỗi trong quá trình lấy dữ liệu.")
    window.location.href = "/";
}

$(document).ready(function(){
    $(".dropdown_toggle").click(function(e){
        let dropdown_content = $(this).parent().children(".dropdown_content");
        dropdown_content.slideToggle();
    });

    $("[subject-id]").click(function(e){
        let csrftoken = getCookie('csrftoken');
        let url = "/api/score";
        uni_id = $("#subject").attr("university-id");
        let data = {csrfmiddlewaretoken : csrftoken, university : uni_id};
        subj_id = $(this).attr("subject-id");
        if(subj_id != 0){
            data.subject = subj_id
        }              
        ajax_request(data, "POST", "json", url, success_callback, error_callback);
    });

    (function(){
        let csrftoken = getCookie('csrftoken');
        let url = "/api/score";
        let data = {csrfmiddlewaretoken : csrftoken, university : 24};
        ajax_request(data, "POST", "json", url, success_callback, error_callback);
    })();

    
})

function ajax_request(data_, type_, data_type_, url_, success_, error_){
    return $.ajax({
        cache : false,
        async : true,
        type : type_,
        dataType : data_type_,
        url : url_,
        data : data_,
        success : function(response){
            success_ != null && success_(response);
        },
        error : function(response){
            error_ !=null && error_(response);
        }
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function print_response(response){
    console.log(response);
}

function login_success_reload(response){
    if(response.success == true){
        window.location.reload()
    }else{
        if(response.__all__){
            let message = (response.__all__)[0].message;
            $("#login_errors").text(message) ;
        }
    }
}

function register_success(response){
    let error_dom = $("#signup_errors"), success_dom = $("#signup_success");
    error_dom.empty();
    success_dom.empty();
    if(response.success == true){
        success_dom.text("Đăng ký thành công !");
        success_dom.empty();
    }else{
        $.each(response,function(field, errors){
            let list_error = "";
            list_error += field + " :<ul>";
            $.each(errors,function(code,error){
                list_error += "<li>" + error.message + "</li>";
            });
            list_error += "</ul>";
            error_dom.append(list_error);
        });
    }
}

$(document).ready(function(){
    $("#login").submit(function(e){
        e.preventDefault();
        let csrftoken = getCookie('csrftoken');
        let data = $(this).serializeArray();
        data.push({ name: 'csrfmiddlewaretoken', value: csrftoken });
        let url = "/api/auth";
        ajax_request(data, "POST", "json", url, login_success_reload, print_response);
    });

    $("#signup").submit(function(e){
        e.preventDefault();
        let data = $(this).serialize();
        let url = "/api/register";
        ajax_request(data, "POST", "json", url, register_success, print_response);
    });

    $(".modal").on("hidden.bs.modal", function(){
        $(this).find("input").val("");
        $(".alert").empty();
    });
})
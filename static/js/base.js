$(document).ready(function() {
  $('#example').DataTable(); $('[data-toggle="tooltip"]').tooltip(); $('.showlater').hide().show(4000); jQuery('.fadein').hide().fadeIn(8000); 
  jQuery('.hoveranim').hover(function() {
    jQuery('.hoveranim').animate({left:"300px"});

  });
  window.onscroll=function(){ scroll()};
  function scroll(){
    if(document.body.scrollTop>20 || document.documentElement.scrollTop > 20) {
      $('#gotop').css({"display":"block"});   
    }
    else $('#gotop').css({"display":"none"});
  }
  jQuery('#gotop').click(function(){
    jQuery('html, body').animate({
      scrollTop: jQuery('body').offset().top
                    // document.documentElement.scrollTop = 0;

                  }, 250);
  });
  jQuery('.count').each(function() {
    jQuery(this).prop('Counter', 0).animate({
      counter: jQuery(this).text()}, {duration: 4000, easing:'swing',step: function(now) {
        jQuery(this).text(Math.ceil(now));
      }
    });
  });
  // jQuery('.sortable').DataTable({
    /*"columnDefs": [{
      "targets" : "no-sort",
      "orderable" : false,
    }]*/
    // "pageLength": 25,
    // "info": "Đang thể hiện từ trường số _START_ tới trường số _END_ trren tổng số _TOTAL_ trường",
    // "lengthMenu": "Số trường trên bảng: _MENU_ trường.",
    // "paginate" : {
      // "next" : "Trang sau",
      // "previous" : "Trang trước",
    // },
    // "search" : "Tìm kiếm: ",
  // });
});
jQuery(document).on('click', '.go-to-id', function(){
  jQuery(jQuery(this).attr('show')).show();
  jQuery('html, body').animate({
    scrollTop: jQuery(jQuery(this).attr('href')).offset().top
  }, 250);
});


function ajax_request(cache_, async_, type_, data_type_, url_, headers_, data_, success_, error_){
    return $.ajax({
        cache : cache_,
        async : async_,
        type : type_,
        dataType :  data_type_,
        headers : headers_,
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
    let login_error_dom =$("#login_errors").empty()
    if(response.success == true){
        window.location.reload()
    }else{
        list_error = message_to_html(response)
        login_error_dom.append(list_error)
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
        let list_error = message_to_html(response)
        error_dom.append(list_error);
    }
}

function message_to_html(message){
    let list_error = "";
    $.each(message,function(field, errors){
        list_error += field + " :<ul>";
        $.each(errors,function(code,error){
            list_error += "<li>" + error.message + "</li>";
        });
        list_error += "</ul>";
    });
    return list_error;
}

$(document).ready(function(){
    $("#login").submit(function(e){
        e.preventDefault();
        let csrftoken = getCookie('csrftoken');
        let data = $(this).serializeArray();
        data.push({ name: 'csrfmiddlewaretoken', value: csrftoken });
        let url = "/api/auth";
        ajax_request(false, true, "POST", "json", url, null, data, login_success_reload, print_response);
    });

    $("#signup").submit(function(e){
        e.preventDefault();
        let csrftoken = getCookie('csrftoken');
        let data = $(this).serializeArray();
        data.push({ name: 'csrfmiddlewaretoken', value: csrftoken });
        let url = "/api/register";
        ajax_request(false, true, "POST", "json", url, null, data, register_success, print_response);
    });

    $(".modal").on("hidden.bs.modal", function(){
        $(this).find("input").val("");
        $(".alert").empty();
    });
})

function ajax_request(cache_, async_, type_, data_type_, url_, headers_, data_, success_, error_){
    return $.ajax({
        cache : cache_,
        async : async_,
        type : type_,
        dataType :  data_type_,
        headers : headers_,
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
    let login_error_dom =$("#login_errors").empty()
    if(response.success == true){
        window.location.reload()
    }else{
        list_error = message_to_html(response)
        login_error_dom.append(list_error)
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
        let list_error = message_to_html(response)
        error_dom.append(list_error);
    }
}

function message_to_html(message){
    let list_error = "";
    $.each(message,function(field, errors){
        list_error += field + " :<ul>";
        $.each(errors,function(code,error){
            list_error += "<li>" + error.message + "</li>";
        });
        list_error += "</ul>";
    });
    return list_error;
}

$(document).ready(function(){
    $("#login").submit(function(e){
        e.preventDefault();
        let csrftoken = getCookie('csrftoken');
        let data = $(this).serializeArray();
        data.push({ name: 'csrfmiddlewaretoken', value: csrftoken });
        let url = "/api/auth";
        ajax_request(false, true, "POST", "json", url, null, data, login_success_reload, print_response);
    });

    $("#signup").submit(function(e){
        e.preventDefault();
        let csrftoken = getCookie('csrftoken');
        let data = $(this).serializeArray();
        data.push({ name: 'csrfmiddlewaretoken', value: csrftoken });
        let url = "/api/register";
        ajax_request(false, true, "POST", "json", url, null, data, register_success, print_response);
    });

    $(".modal").on("hidden.bs.modal", function(){
        $(this).find("input").val("");
        $(".alert").empty();
    });
})

// function ajax_request(data_, type_, data_type_, url_, success_, error_){
//   return $.ajax({
//     cache : false,
//     async : true,
//     type : type_,
//     dataType : data_type_,
//     url : url_,
//     data : data_,
//     success : function(response){
//       success_ != null && success_(response);
//     },
//     error : function(response){
//       error_ !=null && error_(response);
//     }
//   });
// }

// function getCookie(name) {
//   var cookieValue = null;
//   if (document.cookie && document.cookie !== '') {
//     var cookies = document.cookie.split(';');
//     for (var i = 0; i < cookies.length; i++) {
//       var cookie = jQuery.trim(cookies[i]);
//       if (cookie.substring(0, name.length + 1) === (name + '=')) {
//         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//         break;
//       }
//     }
//   }
//   return cookieValue;
// }

// function print_response(response){
//   console.log(response);
// }

// function login_success_reload(response){
//   let login_error_dom =$("#login_errors").empty()
//   if(response.success == true){
//     window.location.reload()
//   }else{
//     list_error = message_to_html(response)
//     login_error_dom.append(list_error)
//   }
// }

// function register_success(response){
//   let error_dom = $("#signup_errors"), success_dom = $("#signup_success");
//   error_dom.empty();
//   success_dom.empty();
//   if(response.success == true){
//     success_dom.text("ÄÄƒng kĂ½ thĂ nh cĂ´ng !");
//     success_dom.empty();
//   }else{
//     let list_error = message_to_html(response)
//     error_dom.append(list_error);
//   }
// }

// function message_to_html(message){
//   let list_error = "";
//   $.each(message,function(field, errors){
//     list_error += field + " :<ul>";
//     $.each(errors,function(code,error){
//       list_error += "<li>" + error.message + "</li>";
//     });
//     list_error += "</ul>";
//   });
//   return list_error;
// }

// $(document).ready(function(){
//   $("#login").submit(function(e){
//     e.preventDefault();
//     let csrftoken = getCookie('csrftoken');
//     let data = $(this).serializeArray();
//     data.push({ name: 'csrfmiddlewaretoken', value: csrftoken });
//     let url = "/api/auth";
//     ajax_request(data, "POST", "json", url, login_success_reload, print_response);
//   });

//   $("#signup").submit(function(e){
//     e.preventDefault();
//     let csrftoken = getCookie('csrftoken');
//     let data = $(this).serializeArray();
//     data.push({ name: 'csrfmiddlewaretoken', value: csrftoken });
//     let url = "/api/register";
//     ajax_request(data, "POST", "json", url, register_success, print_response);
//   });

//   $(".modal").on("hidden.bs.modal", function(){
//     $(this).find("input").val("");
//     $(".alert").empty();
//   });
// })

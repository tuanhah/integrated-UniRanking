$(function() {

    jQuery(window).resize(function(){
        var wid = jQuery(window).width();
        jQuery('.jumbo').css({'width':wid});
    });
});
$(function() {

	jQuery(window).resize(function(){
		var wid = jQuery(window).width();
		jQuery('.jumbo').css({'width':wid});
	});
});
function scroll_into_viewport(element){
	let element_top = $(element).offset().top;
	let element_bottom = element_top + $(element).outerHeight();
	let window_top = $(window).scrollTop();
	let window_bottom = window_top + $(window).height();
	return ((element_top <= window_bottom && element_bottom >= window_bottom) || (element_bottom >= window_top && element_top <= window_top));
}
$(document).ready(function(){
	// $(window).scroll(function(){
		// if(scroll_into_viewport('#info_area')) {
			jQuery('.count').each(function() {
				jQuery(this).prop('Counter', 0).animate({
					counter: jQuery(this).text()}, {duration: 10000, easing:'swing',step: function(now) {
						jQuery(this).text(Math.ceil(now));
					}
				});
			});
		// }
	// });
	$('.showlater').hide().show(10000);
	$('.fadein').hide().fadeIn(8000);
});
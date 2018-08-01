$.fn.isOnViewport = function() {
	let wind = $(window);
	let viewport = {
		top : wind.scrollTop(),
		left : wind.scrollLeft()
	};
	viewport.right = viewport.left + wind.width();
	viewport.bottom = viewport.top + wind.height();

	let bounds = this.offset();
	bounds.right = bounds.left + this.outerWidth();
	bounds.bottom = bounds.top + this.outerHeight(); 

	return (!(viewport.right < bounds.left || viewport.left > bounds.right || viewport.bottom < bounds.top || viewport.top > bounds.bottom));
};

// function scroll_into_viewport(element){
// 	let element_top = $(element).offset().top;
// 	let element_bottom = element_top + $(element).outerHeight();
// 	let window_top = $(window).scrollTop();
// 	let window_bottom = window_top + $(window).height();
// 	return ((element_top <= window_bottom && element_bottom >= window_bottom) || (element_bottom >= window_top && element_top <= window_top));
// }

$(document).ready(function(){
	// $('#home__title').show().addClass('animated bounceInDown');
	// $('#home__title__description').show().addClass('animated bounceInUp');

    $('.navbar-toggler').click(function() {
    	if(!$(window).scrollTop()) {
    		$('#navibar').toggleClass('navbar__over');
    	}
    });

	$(window).resize(function(){
		let height = $(window).height() - $('#navibar').height();
		$('.home__view').css({'height': height});
	});
	$(window).on('scroll', function() {
		if($(window).scrollTop()) {
			$('#navibar').addClass('navbar__over');
		}
		else {
			$('#navibar').removeClass('navbar__over');
		};
		if($('.showlater').isOnViewport()) {
			$('.showlater').show().addClass('animated bounceInRight');			
		};
		if($('#carousel-id').isOnViewport()) {
			$('#carousel-id').addClass('animated bounceInLeft');
		};
		if($('.main-function').isOnViewport()) {
			$('.main-function').addClass('animated flipInX');
		};
		if($('.count').isOnViewport()){}

	});
	
	$('.count').each(function() {
		$(this).prop('Counter', 0).animate({
			counter: $(this).text()}, {duration: 10000, easing:'swing',step: function(now) {
				$(this).text(Math.ceil(now));
			}
		});
	});
});
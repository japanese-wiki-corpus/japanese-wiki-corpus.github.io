
// close navbar when click outside
$(document).ready(function () {
	$(document).click(function (event) {
		var clickover = $(event.target);
		var _opened = $(".navbar-collapse").hasClass("show");
		if (_opened === true && !clickover.parents().hasClass("navbar-collapse")) {
			$(".navbar-toggler").click();
		}
	});
});

// jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});

$('#main-collapsible').on('show.bs.collapse', function () {
	$('#main-navbar').css("background-color", "black");
});
$('#main-collapsible').on('hidden.bs.collapse', function () {
	$('#main-navbar').css("background-color", "transparent");
});


const gcseInitCallback = function() {
	$('.gstl_50').attr('style', 'position: fixed !important');
	$('.nav-search .gstl_50').attr('style', 'position: relative !important');
	$('table.gsc-search-box td.gsc-input').attr('style', 'padding: 0px');
	$('.gsc-input-box').attr('style', 'padding: 3px 0px;');
	$('.gsc-search-button-v2').attr('style', 'padding: 10px 17px; margin: 0;');
};
window.__gcse = {
  parsetags: 'onload',
  initializationCallback: gcseInitCallback
};

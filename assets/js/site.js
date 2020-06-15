
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

console.log(window.parent.location);

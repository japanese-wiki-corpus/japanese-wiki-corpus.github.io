var checkExist = setInterval(function() {
	if ($('.ap_container').height() > 50) {
		console.log($('.ap_container').height());
		$('.ap_container').attr('style', 'border-style: solid; border-width: medium; width: fit-content; margin: 40 0;');
		clearInterval(checkExist);
	}
}, 100); // check every 100ms
setTimeout(function(){ clearInterval(checkExist); }, 10000);

$(window).on('load', function(){

// Facebook buttons
(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
	js.async=true;
    js.src = "https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.6";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));
  
});

if (document.getElementById("main-text").scrollHeight - 100 <= document.body.clientHeight) {
	document.getElementById("social-footer").style.display = "none";
}

$(window).on('load', function(){

$('.ap_container').each(function() {
  if ($(this).height() > 50) { 
	$(this).attr('style', 'border: 1px solid rgba(0,0,0,.1); margin: 40 0; width: fit-content;');
  }
});

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

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
  
  $('.ap_container').attr('style', 'border-style: solid; width: fit-content; margin: 20 0;');
  
});

if (document.getElementById("main-text").scrollHeight - 100 <= document.body.clientHeight) {
	document.getElementById("social-footer").style.display = "none";
}

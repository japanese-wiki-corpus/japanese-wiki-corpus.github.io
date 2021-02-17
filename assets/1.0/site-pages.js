$(window).on('load', function(){

$('.ap_container').each(function() {
  console.log($( this ).height());
  if ($(this).height() > 10) { 
	$(this).attr('style', 'border-style: solid; border-width: medium; margin: 40 0; width: fit-content;');
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

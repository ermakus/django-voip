// This script is preprocessed by Django 
var user = false;

function reload() {
   $('#player').show();
   $.getJSON( "/room/context", null, function( context ) {
        	if( context ) {
			user = context.user;
			$("#username").html( context.user );
			$('.authorized').show();
			$('.unauthorized').hide();
		} else {
			$('.authorized').hide();
			$('.unauthorized').show();
		}
  });
}

function login( next ) {
	var embed = '';
	if( next.indexOf("/social/login") == 0 ) next='/';
	if( next.indexOf("embed=yes") ) embed='&embed=yes';
	$.fancybox({
			'padding'		: 10,
			'width'		        : 500,
			'href'			: '/social/login/?next=' + escape( next ) + embed,
			'type'			: 'iframe',
			'scrolling' : 'no',
                        'onClosed' : reload,
		});
	return false;
}

function popup( href ) {
        if( href.indexOf('/accounts/register') == 0 || user )
                 $.fancybox({
			'padding'		: 10,
			'width'		        : 500,
			'href'			: href,
			'type'			: 'iframe',
                        'onClosed' : reload,
	}); else login( href  );
}

// Common initialization
$(document).ready(function() {

	$('body').ajaxError(function(e, r, settings){
   		alert("Server connection failed.\nURL: " + settings.url);
	});

        $('.act').click( function() {
		popup( $(this).attr('href') + '?embed=yes' );
		return false;
	} );
        reload();
});
	

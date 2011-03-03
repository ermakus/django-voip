// This script is preprocessed by Django 
var user = false;

function reload() {
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
			'height'		: 460,
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
			'width'		        : 550,
			'height'		: 450,
			'href'			: href,
			'type'			: 'iframe',
                        'onClosed' : reload,
	}); else login( href  );
}

function drawer( href ) {
       if( $('#drawer').height() > 0 ) return drawer_close();
       $('#drawer_iframe').attr("src",href);
       $("#drawer").animate({
                        height: "600px"
                })
                .animate({
                        height: "500px"
                }, "fast" );
                $(".drawer_button").toggle();
}

function drawer_close() {
                $("#drawer").animate({
                        height: "0px"
                }, "fast");
                $(".drawer_button").toggle();
}

function status(message) {
	$("#status").html( message );
}

// Common initialization
$(document).ready(function() {

	$('body').ajaxError(function(e, r, settings){
   		alert("Server connection failed.\nURL: " + settings.url);
	});

        $('.act').click( function() {
		drawer( $(this).attr('href') + '?embed=yes' );
		return false;
	} );

        $('#search').focus( function() {
                $(this).attr('value','');
        });

        $('#nav ul li').each( function() {
                var href = $(this).children(':first-child').attr('href');
		if( window.location.pathname == href ) $(this).addClass('current');
        } );

	$('.protected').click(function(){
                if( user ) return true;
		 var href = $(this).children(':first-child').attr('href');
		drawer("/social/login?embed=yes&next=" + href );
		return false;
	});

	$("#drawer_on").click(function(){
		drawer("/social/login?embed=yes");
        });

	$("#drawer_off").click(function(){
		drawer_close();
	});


        reload();
});
	

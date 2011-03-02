	var path    = window.location.pathname;
   	var server    = "localhost";
        var comet_port = 9999;
        var TCPSocket = Orbited.TCPSocket;
	var client = new STOMPClient();

	jQuery.extend(jQuery.expr[':'], {
    		focus: function(element) { 
        		return element == document.activeElement; 
    		}
	});

        $( function() {
		status("Connecting...");
		client.onopen = function() {
			status("You connected to: " + window.location.pathname );
    			window.onbeforeunload = function() {
        			client.unsubscribe( window.location.pathname );
        			client.disconnect(); 
    			};
    		};

    		client.onclose = function(c) {
			status("Connection lost, Code:" + c);
    		};
    		client.onerror = function(error) {
        		status("ERROR: " + error); 
    		};

    		client.onerrorframe = function(frame) {
        		status("ERROR FRAME:  " + frame.body); 
    		};

    		client.onconnectedframe = function() {
        		client.subscribe( window.location.pathname );
    		};

    		client.onmessageframe = function(frame) { //check frame.headers.destination?
			var msg = eval( "(" + frame.body + ")" );
			update( msg );
    		};

    		var cookie = $.cookie("sessionid");
    		client.connect(server, comet_port, "dude", cookie);

		$('#_content').keypress( function(event) {
			if ((event.keyCode || event.which) == 13) { 
				var msg = {};
                                msg.content = $(this).attr('value');
				msg.kind    = "message"
				send(msg);
				$(this).attr('value','');
				return false; 
			}
		}).bind('focus',function() {
			scrollme();
    		});

		$('#_button_bunch').click( function() {
				var msg = {};
				msg.content = $('#_content').attr('value');
				msg.kind    = "message"
				send(msg);
				$('#_content').attr('value','');
		});

    	} );
   
	function scrollme() {
		var msg = $('#_content');
		if( msg.is(':focus') ) {
			var offset = $('body').height() - 30;
			$(window).scrollTop( offset );
		}
	}
 
	function send(msg) {
		client.send( JSON.stringify(msg), path );
	}
	
	function update(msg) {
	       	var html = ( "<div id='" + msg.uid + "' class='" + msg.kind + "'>" + msg.content + "</div>" );
		$( '#' + bunch.uid + "-children").append( html );
		scrollme();
	}


	var path    = window.location.pathname;
   	var server    = "localhost";
        var comet_port = 9999;
        var TCPSocket = Orbited.TCPSocket;
	var client = new STOMPClient();
        var selected = false;

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

		$('#input_content').keypress( function(event) {
			if ((event.keyCode || event.which) == 13) { 
				var msg = {};
                                msg.content = $(this).val();
				msg.kind    = "message"
				msg.uid     = "!auto";
				send(msg);
				$(this).attr('value','');
				return false; 
			}
		}).bind('focus',function() {
			scrollme();
    		});

		$('#button_bunch').click( function() {
				var msg = {};
				msg.content = $('#input_content').val();
				msg.kind    = "message"
				send(msg);
				$('#input_content').attr('value','');
		});

		$('#button_delete').click( function() {
			if( selected ) {
				var msg = {};
				msg.uid  = selected.attr('id');
				msg.kind = "delete"
				send(msg);
			}
			return false;
		});


		$("#pwd>li>ul").append("<li id='new' class='new'>Bunch!</li>");

		$("#pwd>li>ul>li").live( 'click', function() { 
			var id = $(this).attr("id");  
			if( $(this).hasClass('selected') && id != "new") {
				window.location.href = document.location.href + id;
				return true;
			}
			select( id );
		});

		select("new");
    	} );
  

        function select( id ) {
			var li = $('#'+id);
                        if( li.length == 0 ) {
				$("#commands").appendTo( $("#new") ).show();
				$('#input_content').html( "" );
				selected = false;
				return;
			} else {
				if(selected) selected.removeClass("selected");
				li.addClass("selected");
				selected = li;
				$("#commands").appendTo( li ).show();
                                var val = li.children("p").html();
				$('#input_content').val( val ).focus();
			}
	
        }
 
	function scrollme() {
		var msg = $('#input_content');
		if( msg.is(':focus') ) {
			var offset = $('html').height(); 
			$(window).scrollTop( offset );
		}
	}
 
	function send(msg) {
		msg.parent = path;
		client.send( JSON.stringify(msg), path );
	}
	
	function update(msg) {
		var li = $('#'+msg.uid);
		if( msg.kind == "delete" ) 
		{
			if( li.next().length ) select( li.next().attr( "id" ) ); else select("new");
			$("#" + msg.uid ).remove();
		} 
		else 
		{
	       		var html = $( "<li id='" + msg.uid + "' class='" + msg.kind + "'><p>" + msg.content + "</p><ul id='" + msg.uid + "-children'></ul></li>" );
			if( !li.length ) html.insertBefore( $('#new') ); else li.replaceWith( html );
			scrollme();
		}
	}


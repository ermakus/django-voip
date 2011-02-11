// AutoBot is who respond players messages

var sys  = require('sys'),
    faye = require('./faye');

var client = new faye.Client('http://localhost:9000/comet');

client.subscribe('/action', function(message) {
  sys.puts( "User: " + message );
  client.publish('/event', "pong" ); 
});

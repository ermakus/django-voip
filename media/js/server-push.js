Server = {
  // Init game and connect server
  connect: function(url) {
    this._comet = new Faye.Client( url + '/comet');
  },

  // Init GUI
  subscribe: function(stream, handler) {
    this._comet.subscribe('/' + stream, handler );
  },

  // Send message to game server
  send: function(stream, message) {
    this._comet.publish('/' + stream , message);
  },
};


$(document).ready(function(){
  var socket = io.connect();

  // the socket.io documentation recommends sending an explicit package upon connection
  socket.on('connect', function() {
    socket.emit('connect', {data: 'I\'m connected!'});
    });

  socket.on('update value', function(msg) {
    console.log(msg);
    //console.log('About to change the value of ' + msg.who + ' from ' + $('input#'+msg.who).is(':checked') + ' to ' + msg.data);
    //$('input#'+msg.who).prop("checked",(msg.data));
  });

  socket.on('update bet', function(msg) {
    console.log(msg);
    var data = JSON.parse(msg);
    // The JSON should look something like this:
    //{'horse_id : 1, 'bettor' : 1, 'amount' : 1, 'ago' : 'Just Now'}

    $('td#person'+data.horse_id).html(data.bettor);
    $('td#bet'+data.horse_id).html(data.amount);
    $('td#ago'+data.horse_id).html('$' + data.ago);
  });

  socket.on('insert row', function(msg) {
    var data = JSON.parse(msg)
    var $html = '<tr>\
      <td>' + data.horse_name + '(' + data.horse_nickname + ')</td>\
      <td>No one</td>\
      <td>$0</td>\
      <td>Never</td></tr>'
    $('#curBetsTable TBODY').append($html)
  });

});

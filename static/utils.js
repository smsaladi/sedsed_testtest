var socket;

$(document).ready(function() {
    socket = io.connect('//' + document.domain + ':' + location.port + '/shell', {secure: true});
    socket.on('connect', function() {
        socket.emit('joined', {});
    });
    socket.on('message', function(data) {
        $('#shell').val($('#shell').val() + data.msg + '\n');
        $('#shell').scrollTop($('#shell')[0].scrollHeight);
    });
    socket.on('status', function(data) {
        $('#shell').val($('#shell').val() + '<' + data.msg + '>\n');
        $('#shell').scrollTop($('#shell')[0].scrollHeight);
    });
    $('#text').keypress(function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            text = $('#text').val();
            $('#text').val('');
            socket.emit('comando', {msg: text});
        }
    });
});

function leave_room() {
    socket.disconnect();
    window.location.href = "http://www.google.com";
}


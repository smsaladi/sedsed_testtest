#!/usr/bin/env python

"""
A webshell modified to only interact with sedsed

Intially based on the code here:
https://gist.github.com/phoemur/461c97aa5af5c785062b7b4db8ca79cd

Author: Shyam Saladi (smsaladi@gmail.com)
Date: November 2018
"""

import os
import subprocess
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['DEBUG'] = bool(os.environ['SECRET_KEY'])
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('shell.html')

@socketio.on('joined', namespace='/shell')
def joined(message):
    send_status('SUCCESSFULLY CONNECTED')
    
@socketio.on('comando', namespace='/shell')
def comando(comando):
    c = comando['msg']
    send_text('$ ' + c)
    print(c)

    if not c.startswith('sed'):
        c = c + 'sed'
        send_text("Don't forget to include sed!")
        send_text("Trying: " + c)

    try:
        b = subprocess.check_output(c, shell=True).decode()
    except Exception as err:
        b = str(err)
        
    send_text(b)

def send_status(msg):
    emit('status', {'msg': msg})

def send_text(msg):
    emit('message', {'msg': msg})
    
if __name__ == '__main__':
    socketio.run(app)
    

#! /usr/bin/env python3

import os
import logging
from flask_socketio import SocketIO
from flask import Flask, render_template, url_for


logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
socketio = SocketIO(app)


@app.context_processor
def override_url_for():
    return(dict(url_for=dated_url_for))


def dated_url_for(endpoint, **values):
    '''
    This is uses to overide the normal cache for loading static resources.
    '''
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                    endpoint,
                                    filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/', methods=['GET'])
def main_page():
    ''' Used to get the control panel page. '''
    return(render_template('chatroom.html'))

# 
@socketio.on('join_chatroom')
def join_chatroom():
    '''
    '''
    if chatBackup != []:
        fmtChatHistory = ""
        for data in chatBackup:
            fmtChatHistory += '<li>{0} : {1}</li><br>'.format(
                data[0],
                data[1])

        socketio.emit('new_join', fmtChatHistory)

# 
@socketio.on('send_message')
def send_message(data):
    '''
    '''
    chatBackup.append([data['username'], data['message']])

    fmntMsg = '<li>{0} : {1}</li><br>'.format(
        data['username'],
        data['message'])
    
    socketio.emit('new_message', fmntMsg)


if __name__ == '__main__':                
    socketio.run(app)
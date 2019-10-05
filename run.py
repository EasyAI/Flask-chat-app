#! /usr/bin/env python3

import os
import logging
from flask_socketio import SocketIO
from flask import Flask, render_template, url_for

## Current output status for messages.
logging.basicConfig(level=logging.INFO)

## List to store past messages/names.
chatBackup = []

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
    ''' Used to get the chatroom.html page '''
    return(render_template('chatroom.html'))


@socketio.on('join_chatroom')
def join_chatroom():
    '''
    If a chatroom is joined then all the previous messages will be sent out again.
    '''
    if chatBackup != []:
        fmtChatHistory = ""
        for data in chatBackup:
            fmtChatHistory += '<li>{0} : {1}</li><br>'.format(
                data[0],
                data[1])

        socketio.emit('new_join', fmtChatHistory)


@socketio.on('send_message')
def send_message(data):
    '''
    If a message is sent, its username and message will be saved to a list.
    '''
    message = sanitised(data['message'])
    chatBackup.append([data['username'], message])

    fmntMsg = '<li>{0} : {1}</li><br>'.format(
        data['username'],
        message)
    
    socketio.emit('new_message', fmntMsg)


def sanitised(message):
    '''
    Super basic way to sanitise a message by eliminating angle brackets.
    '''

    sMessage = message

    sMessage = (message.replace('<', ' ')).replace('>', ' ')
    sMessage = (message.replace('{', ' ')).replace('}', ' ')

    return(sMessage)

if __name__ == '__main__':                
    socketio.run(app)
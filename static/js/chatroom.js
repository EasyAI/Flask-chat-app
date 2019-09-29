var socket = io('http://127.0.0.1:5000');
var username = '';

$(document).ready(function() {
    // Setup the socket server ip/port

    socket.on('connect', function() {
        socket.emit('join_chatroom');
    });

    socket.on('new_join', function(data) {
        $('#message-list').html(data);
    });

    socket.on('new_message', function(data) {
        $('#message-list').append(data);
    });
});

function setUsername(form) {

    username = form.textInput.value;
}

function sendMessage(form) {

    if (username != '') {

        messageData = {
            'username': username,
            'message': form.textInput.value
        };

        socket.emit('send_message', messageData);
    } else {
        alert('A username must be set first.')
    }
}
var socket = io.connect()


function pretty_text(user, user_message){
    let text = `<div class="custom">
        <p class="custom_name">${user}</p> 
        <p class="custom_text">${user_message}</p>
    </div>`;
    return text;
}

function alerts(message_alert){
    let text = `
    <div class="alert alert-danger" role="alert">
    ${message_alert}
    </div>
    `
    return text;
}

function joinRoom() {
    var room = document.getElementById('roomID').value;
    var joinbtn = document.getElementById('jointbn');
    if(room <= 0){
        var alertArea = document.getElementById('alert_area');
        alertArea.innerHTML += alerts("Room number can't be lower or equal to 0");
        joinbtn.setAttribute('disabled', '');
        return
    }

    var roomnumber = document.getElementById('room-id');
    roomnumber.innerHTML = room;
    
    socket.emit('join', {'room': room});

    
    joinbtn.setAttribute('disabled', '');
}

function leaveRoom() {
    var room = document.getElementById('roomID').value;
    socket.emit('leave', {'room': room});
    var messages = document.getElementById('chat-area');

    var divs = messages.getElementsByTagName("div");

        for (var i = divs.length - 1; i >= 0; i--) {
            divs[i].remove();
        }
    location.reload()
}

function sendMessage() {
    var room = document.getElementById('roomID').value;
    var message = document.getElementById('text-message').value;
    socket.emit('message', {'room': room, 'msg': message});
    document.getElementById('text-message').value = '';
}

socket.on('mm', function(data) {
    var messages = document.getElementById('chat-area');

    user = data['user'];
    user_message = data['msg'];

    messages.innerHTML += pretty_text(user, user_message);
});

socket.on('load_messages', function(data) {
    var messages = data.messages;
    updateMessages(messages);
});

function updateMessages(messages) {
    var messageContainer = document.getElementById('chat-area');

    messageContainer.innerHTML = '';

    for (var i = 0; i < messages.length; i++) {
        var message = messages[i];
        var prettyText = pretty_text(message[0], message[1]);
        messageContainer.innerHTML += prettyText;
    }
}
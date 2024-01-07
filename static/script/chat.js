var socket = io.connect()

function pretty_text(user_name, message){
    let tmp_text = `<div class="custom">
        <p class="custom_name">${user_name}</p> 
        <p class="custom_text">${message}</p>
    </div>`;
    return tmp_text;
}

function alerts(message){
    let tmp_text = `
    <div class="alert alert-danger" role="alert">
    ${message}
    </div>`
    return tmp_text;
}

function joinRoom() {
    var room_number = document.getElementById('roomID').value;
    var join_button = document.getElementById('jointbn');
    if(room_number <= 0){
        var alertArea = document.getElementById('alert_area');
        alertArea.innerHTML += alerts("Room number is incorrect!");
        join_button.setAttribute('disabled', '');
        return
    }
    var roomnumber = document.getElementById('room-id');
    roomnumber.innerHTML = room_number;
    socket.emit('join', {'room': room_number});
    join_button.setAttribute('disabled', '');
}

function leaveRoom() {
    var room_number = document.getElementById('roomID').value;
    socket.emit('leave', {'room': room_number});
    var messages = document.getElementById('chat-area');
    var divs = messages.getElementsByTagName("div");
        for (var i = divs.length - 1; i >= 0; i--) {
            divs[i].remove();
        }
    location.reload()
}

function sendMessage() {
    var room_number = document.getElementById('roomID').value;
    var user_message = document.getElementById('text-message').value;
    socket.emit('message', {'room': room_number, 'msg': user_message});
    document.getElementById('text-message').value = '';
}

socket.on('mm', function(data) {
    var all_messages = document.getElementById('chat-area');
    user_name = data['user'];
    user_message = data['msg'];
    all_messages.innerHTML += pretty_text(user_name, user_message);
});

socket.on('load_messages', function(data) {
    var all_messages = data.messages;
    updateMessages(all_messages);
});

function updateMessages(all_messages) {
    var messageContainer = document.getElementById('chat-area');
    messageContainer.innerHTML = '';
    for (var i = 0; i < all_messages.length; i++) {
        var message = all_messages[i];
        var prettyText = pretty_text(message[0], message[1]);
        messageContainer.innerHTML += prettyText;
    }
}
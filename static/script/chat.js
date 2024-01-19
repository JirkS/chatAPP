var webSocket = io.connect()

function createHtmlTagMessage(user_name, message){
    let tmp_text = `<div class="custom">
        <p class="custom_name">${user_name}</p> 
        <p class="custom_text">${message}</p>
    </div>`;
    return tmp_text;
}

function messageAlert(message){
    let tmp_text = `
    <div class="alert alert-danger" role="alert">
    ${message}
    </div>`
    return tmp_text;
}

function sendMessage() {
    var roomNumber = document.getElementById('roomID').value;
    var userMessage = document.getElementById('text-message').value;
    webSocket.emit('message', {'room': roomNumber, 'msg': userMessage});
    document.getElementById('text-message').value = '';
}

function updateMessages(all_messages) {
    var messagesBox = document.getElementById('chat-area');
    messagesBox.innerHTML = '';
    for (var i = 0; i < all_messages.length; i++) {
        var m = all_messages[i];
        var htmlTag = createHtmlTagMessage(m[0], m[1]);
        messagesBox.innerHTML += htmlTag;
    }
}

webSocket.on('mm', function(data) {
    var allMessages = document.getElementById('chat-area');
    let userName = data['user'];
    let userMessage = data['msg'];
    allMessages.innerHTML += createHtmlTagMessage(userName, userMessage);
    }
);

webSocket.on('load_messages', function(data) {
    var allmMessages = data.messages;
    updateMessages(allmMessages);
    }
);

function joinRoom() {
    var roomNumber = document.getElementById('roomID').value;
    var joinButton = document.getElementById('jointbn');
    if(roomNumber <= 0){
        var alertsArea = document.getElementById('alert_area');
        alertsArea.innerHTML += messageAlert("Room number is incorrect!");
        joinButton.setAttribute('disabled', '');
        return
    }
    var roomnumber = document.getElementById('room-id');
    roomnumber.innerHTML = roomNumber;
    webSocket.emit('join', {'room': roomNumber});
    joinButton.setAttribute('disabled', '');
}

function leaveRoom() {
    var roomNumber = document.getElementById('roomID').value;
    webSocket.emit('leave', {'room': roomNumber});
    var messages = document.getElementById('chat-area');
    var divs = messages.getElementsByTagName("div");
        for (var i = divs.length - 1; i >= 0; i--) {
            divs[i].remove();
        }
    location.reload()
}
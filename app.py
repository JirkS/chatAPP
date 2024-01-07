from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify, abort
from flask_socketio import SocketIO, join_room, leave_room
from dotenv import load_dotenv
from flask_mysqldb import MySQL
import hashlib
import os

app = Flask(__name__)

app.secret_key = 'kocka'

app.config['MYSQL_DB'] = 'chat'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
mysql = MySQL(app)

socketio = SocketIO(app)

load_dotenv()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["Name"]
        email = request.form["Email"]
        password = request.form["Password"]
        password_confirm = request.form["Password_Confirm"]
        password_hash = hash_password(password)
        password_confirm_hash = hash_password(password_confirm)
        if password_hash == password_confirm_hash:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO users (name, email, password) VALUES(%s, %s, %s)", (username, email, password_hash))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("login"))
        else:
            flash('Passwords do not match. Please try again.', 'warning')
            return render_template("register.html")
    else:
        return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["Email"]
        password = request.form["Password"]

        cursor = mysql.connection.cursor()
        cursor.execute("select * from users where email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password(password, user[3]) and check_email(email, user[2]):
            session["user"] = user
            return redirect(url_for("chat"))
        else:
            flash("Email or password is incorrect!", "warning")
            return render_template("login.html")
    else:
        return render_template("login.html")

def check_password(user_name_password, db_p):
    return hash_password(user_name_password) == db_p
def check_email(user_name_email, db_e):
    return user_name_email == db_e

@app.route("/chat")
def chat():
    if "user" in session:
        return render_template("chat.html")
    else:
        return redirect(url_for("home"))

@app.route("/logout")
def logoff():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.errorhandler(404)
def page_not_found_error(e):
    return render_template('404.html'), 404

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@socketio.on('join')
def join_user(data):
    user_name = session["user"]
    room_number = data['room']
    join_room(room_number)
    socketio.emit('mm', {'user': 'Bot','msg': user_name[1]+' has joined the room!'}, room=room_number)

    messages = get_messages_for_room(room_number)

    socketio.emit('load_messages', {'messages': messages}, room=room_number)

def get_messages_for_room(room_number):
    cursor = mysql.connection.cursor()
    cursor.execute("select users.name, message.MessageText from users inner join message on users.id = message.SenderID where message.RoomID = %s;", (room_number,))
    msg_post = cursor.fetchall()
    if msg_post:
        return msg_post
    else:
        return abort(404)

@socketio.on('leave')
def leave_user(data):
    user_name = session["user"]
    room_number = data['room']
    leave_room(room_number)
    socketio.emit('mm', {'user': 'Bot','msg': user_name[1]+' has left the room!'}, room=room_number)

@socketio.on('message')
def message_user(data):
    user_name = session["user"]
    room_number = data['room']
    message = data['msg']
    socketio.emit('mm', {'user': user_name[1], 'msg': message}, room=room_number)
    cursor = mysql.connection.cursor()
    cursor.execute("insert into message(SenderID, MessageText, RoomID) values(%s, %s, %s)", (user_name[0], message, room_number))
    mysql.connection.commit()
    cursor.close()

@app.route('/chat-api/', methods=['GET'])
def get_all_chat_messages():
    if "user" not in session:
        return redirect(url_for("home"))
    cursor = mysql.connection.cursor()
    cursor.execute("select users.name, users.email, message.MessageText, message.RoomID, message.Timestamp from message inner join users on message.SenderID = users.id order by message.RoomID ")
    msg_post = cursor.fetchall()
    if msg_post:
        return jsonify(msg_post)
    else:
        return abort(404)

@app.route('/chat-api/<name>', methods=['GET'])
def get_chat_messages_by_user(name_user):
    if "user" not in session:
        return redirect(url_for("home"))

    cursor = mysql.connection.cursor()
    cursor.execute("select users.name, users.email, message.MessageText, message.RoomID, message.Timestamp from message inner join users on message.SenderID = users.id where users.name = %s", (name_user,))
    msg_post = cursor.fetchall()
    if msg_post:
        return jsonify(msg_post)
    else:
        return abort(404)

@app.route('/chat-api/<int:id>', methods=['GET'])
def get_chat_messages_by_chat_room(id):
    if "user" not in session:
        return redirect(url_for("home"))
    cursor = mysql.connection.cursor()
    cursor.execute("select users.name, users.email, message.MessageText, message.RoomID, message.Timestamp from message inner join users on message.SenderID = users.id where message.RoomID = %s", (id,))
    msg_post = cursor.fetchall()
    if msg_post:
        return jsonify(msg_post)
    else:
        return abort(404)

@app.route('/chat-api/word/<word>', methods=['GET'])
def get_chat_messages_by_word(w):
    if "user" not in session:
        return redirect(url_for("home"))
    cursor = mysql.connection.cursor()
    cursor.execute("select message.MessageText from message where message.MessageText like %s", ('%' + w + '%',))
    msg_post = cursor.fetchall()
    print(msg_post)
    print("AA")
    if msg_post:
        return jsonify(msg_post)
    else:
        return abort(404)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
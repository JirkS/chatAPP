from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify, abort
from flask_socketio import SocketIO, join_room, leave_room
from dotenv import load_dotenv
from flask_mysqldb import MySQL
import hashlib
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'kocka'

app.config['MYSQL_DB'] = 'chat'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
mysql = MySQL(app)

socketio = SocketIO(app)

error_handler = RotatingFileHandler('logs/errors.log', maxBytes=10000, backupCount=1)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s'))
app.logger.addHandler(error_handler)

info_handler = RotatingFileHandler('logs/info.log', maxBytes=10000, backupCount=1)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s'))
app.logger.addHandler(info_handler)

app.logger.setLevel(min(info_handler.level, error_handler.level))

load_dotenv()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    try:
        if request.method == "POST":
            username = request.form["Name"]
            email = request.form["Email"]
            password = request.form["Password"]
            password_confirm = request.form["Password_Confirm"]
            password_hash = hash_password(password)
            password_confirm_hash = hash_password(password_confirm)
            if password_hash == password_confirm_hash:
                cursor = mysql.connection.cursor()
                cursor.execute("insert into users (name, email, password) values(%s, %s, %s)", (username, email, password_hash))
                mysql.connection.commit()
                cursor.close()
                app.logger.info(f' Info: insert into users executed!')
                return redirect(url_for("login"))
            else:
                flash('Passwords are not same! Try again.', 'warning')
                app.logger.error(f' Error: Passwords are not same!')
                app.logger.info(f' Info: redirect to register successful!')
                return render_template("register.html")
        else:
            app.logger.info(f' Info: redirect to register successful!')
            return render_template("register.html")
    except Exception as e:
        app.logger.error(f' Error: {str(e)}')

@app.route("/login", methods=["POST", "GET"])
def login():
    try:
        if request.method == "POST":
            email = request.form["Email"]
            password = request.form["Password"]
            cursor = mysql.connection.cursor()
            cursor.execute("select * from users where email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            app.logger.info(f' Info: select * from users executed!')
            if user and check_password(password, user[3]) and check_email(email, user[2]):
                session["user"] = user
                app.logger.info(f' Info: redirect to chat successful!')
                return redirect(url_for("chat"))
            else:
                flash("Email or password is incorrect!", "warning")
                app.logger.error(f' Error: Email or password is incorrect!')
                app.logger.info(f' Info: redirect to login successful!')
                return render_template("login.html")
        else:
            app.logger.info(f' Info: redirect to login successful!')
            return render_template("login.html")
    except Exception as e:
        app.logger.error(f' Error: {str(e)}')

def check_password(user_name_password, db_p):
    try:
        return hash_password(user_name_password) == db_p
    except Exception as e:
        app.logger.error(f' Error: {str(e)}')

def check_email(user_name_email, db_e):
    return user_name_email == db_e

@app.route("/chat")
def chat():
    try:
        if "user" in session:
            app.logger.info(f' Info: redirect to chat successful!')
            return render_template("chat.html")
        else:
            app.logger.error(f' Error: User is not in session!')
            app.logger.info(f' Info: redirect to home successful!')
            return redirect(url_for("home"))
    except Exception as e:
        app.logger.error(f' Error: {str(e)}')

@app.route("/logout")
def logoff():
    try:
        session.pop("user", None)
        app.logger.info(f' Info: redirect to home successful!')
        return redirect(url_for("home"))
    except Exception as e:
        app.logger.error(f' Error: {str(e)}')
    
@app.errorhandler(404)
def page_not_found_error(e):
    app.logger.error(f' Error: 404!')
    app.logger.info(f' Info: redirect to 404 successful!')
    return render_template('404.html'), 404

def hash_password(password):
    try:
        return hashlib.sha256(password.encode()).hexdigest()
        app.logger.info(f' Info: password hashed!')
    except Exception as e:
        app.logger.error(f' Error: {str(e)}')

@socketio.on('join')
def join_user(data):
    try:
        user_name = session["user"]
        room_number = data['room']
        join_room(room_number)
        socketio.emit('mm', {'user': 'Bot','msg': user_name[1]+' has joined the room!'}, room=room_number)
        messages = get_messages_for_room(room_number)
        socketio.emit('load_messages', {'messages': messages}, room=room_number)
        app.logger.info(f' Info: message was sent!')
    except Exception as e:
        app.logger.error(f' Error: {str(e)}')

def get_messages_for_room(room_number):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("select users.name, message.MessageText from users inner join message on users.id = message.SenderID where message.RoomID = %s;", (room_number,))
        msg_post = cursor.fetchall()
        if msg_post:
            app.logger.info(f' Info: message was loaded!')
            return msg_post
        else:
            return abort(404)
    except Exception as e:
        app.logger.error(f' Error: {str(e)}')

@socketio.on('leave')
def leave_user(data):
    try:
        user_name = session["user"]
        room_number = data['room']
        leave_room(room_number)
        socketio.emit('mm', {'user': 'Bot','msg': user_name[1]+' has left the room!'}, room=room_number)
        app.logger.info(f' Info: user {user_name[1]} has left the room!')
    except Exception as e:
        app.logger.error(f' Error: {str(e)}')

@socketio.on('message')
def message_user(data):
    try:
        user_name = session["user"]
        room_number = data['room']
        message = data['msg']
        socketio.emit('mm', {'user': user_name[1], 'msg': message}, room=room_number)
        app.logger.info(f' Info: user {user_name[1]} sent message!')
        cursor = mysql.connection.cursor()
        cursor.execute("insert into message(SenderID, MessageText, RoomID) values(%s, %s, %s)", (user_name[0], message, room_number))
        mysql.connection.commit()
        cursor.close()
        app.logger.info(f' Info: insert into message successful!')
    except Exception as e:
        app.logger.error(f' Error: {str(e)}')

@app.route('/chat-api/', methods=['GET'])
def all_messages():
    try:
        if "user" not in session:
            app.logger.error(f' Error: User is not in session!')
            return redirect(url_for("home"))
        cursor = mysql.connection.cursor()
        cursor.execute("select users.name, users.email, message.MessageText, message.RoomID, message.Timestamp from message inner join users on message.SenderID = users.id order by message.RoomID ")
        msg_post = cursor.fetchall()
        if msg_post:
            app.logger.info(f' Info: API - all messages!')
            return jsonify(msg_post)
        else:
            return abort(404)
    except Exception as e:
        app.logger.error(f' Error: {str(e)}')

@app.route('/chat-api/<name>', methods=['GET'])
def messages_by_user(name_user):
    try:
        if "user" not in session:
            app.logger.error(f' Error: User is not in session!')
            return redirect(url_for("home"))
        cursor = mysql.connection.cursor()
        cursor.execute("select users.name, users.email, message.MessageText, message.RoomID, message.Timestamp from message inner join users on message.SenderID = users.id where users.name = %s", (name_user,))
        msg_post = cursor.fetchall()
        if msg_post:
            app.logger.info(f' Info: API - messages by users!')
            return jsonify(msg_post)
        else:
            return abort(404)
    except Exception as e:
        app.logger.error(f' Error: {str(e)}')

@app.route('/chat-api/<int:id>', methods=['GET'])
def messages_by_room(id):
    try:
        if "user" not in session:
            app.logger.error(f' Error: User is not in session!')
            return redirect(url_for("home"))
        cursor = mysql.connection.cursor()
        cursor.execute("select users.name, users.email, message.MessageText, message.RoomID, message.Timestamp from message inner join users on message.SenderID = users.id where message.RoomID = %s", (id,))
        msg_post = cursor.fetchall()
        if msg_post:
            app.logger.info(f' Info: API - all messages by room!')
            return jsonify(msg_post)
        else:
            return abort(404)
    except Exception as e:
        app.logger.error(f' Error: {str(e)}')

@app.route('/chat-api/word/<word>', methods=['GET'])
def messages_by_word(w):
    try:
        if "user" not in session:
            app.logger.error(f' Error: User is not in session!')
            return redirect(url_for("home"))
        cursor = mysql.connection.cursor()
        cursor.execute("select message.MessageText from message where message.MessageText like %s", ('%' + w + '%',))
        msg_post = cursor.fetchall()
        if msg_post:
            app.logger.info(f' Info: API - all messages by word!')
            return jsonify(msg_post)
        else:
            return abort(404)
    except Exception as e:
        app.logger.error(f' Error: {str(e)}')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')

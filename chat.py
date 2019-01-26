from flask import Flask
from flask_socketio import SocketIO
from flask import session, redirect, url_for, render_template, request
from flask import Blueprint
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required
from flask import session
from flask_socketio import emit, join_room, leave_room
from database import db


socketio = SocketIO()
main = Blueprint('main', __name__)
db()

@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    name = session.get('name')
    join_room(room)
    massages = db.select_textMassage(db,room)
    emit('status', {'msg': session.get('name') + ' is now online'}, room=room)
    print(session['history'])
    if session['history'] == 0:
        session['history'] = 1
        for m in massages:
            print(m)
            _,_,s,c,t=m
            emit('message', {'msg': s + '<<' +str(t)+ '>> :' + c}, name=name , room=room)

@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    db.insert_textMassage(db, room, session.get('name'), message['msg'])
    emit('message', {'msg': session.get('name') + '>>' + message['msg']}, room=room)

@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + 'is now offline'}, room=room)


@main.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('.chat'))

@main.route('/<n>/<r>', methods=['GET', 'POST'])
def f(n,r):
    session['name'] = n
    session['room'] = r
    session['history'] = 0
    print(n)
    print(r)
    return redirect(url_for('.chat'))


@main.route('/chat')
def chat():
    name = session.get('name', '')
    room = session.get('room', '')
    return render_template('chat.html', name=name, room=room)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'abc74dkim427_!17#'
app.register_blueprint(main)
socketio.init_app(app)

if __name__ == '__main__':
    socketio.run(app)

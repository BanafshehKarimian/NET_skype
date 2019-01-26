from flask import *
from flaskext.mysql import MySQL
from flask_socketio import SocketIO
import datetime
import redis
from flask_sse import sse
import webbrowser
from database import db
from channel import channel

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'EmpData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')
app.register_blueprint(channel, url_prefix='/channel')
app.config["DEBUG"] = True
connection= mysql.connect()
connection.autocommit=True

db()


@app.route('/')
def signUp():
    if not session.get('logged_in'):
        return render_template('signUp.html')
    else:
        data = db.get_contacts(db,session['username'])
        return render_template('add-contact.html',contacts=data)

@app.route("/create/<Cid>")
def create_page(Cid):
    return render_template("create.html", name=Cid)


@app.route("/join/<Cid>")
def join_page(Cid):
    return render_template("join.html", name=Cid)




@app.route('/logInUser/<Cid>', methods = ['POST'])
def LogInUser(Cid):
    user =  request.values.get('username', '')
    passw = request.values.get('password', '')
    data = db.select_user(db,user,passw)
    if data is None:
        print("Username or Password is wrong")
        return  render_template('signUp.html')
    else:
        #db.insert_user(db,'user1','1234')
        #print(db.select_user(db,'user2','1234'))
        #print(db.select_contact(db,'user1','admin'))
        #db.insert_contact(db,'user1','admin')
        #db.insert_textMassage(db,1,'user1','this is a test msg')
        session['logged_in'] = True		
        session['username'] = user
        data = db.get_contacts(db,user)
        print(data)
        print("Logged in successfully")
        return  render_template('add-contact.html',rows=data)


@app.route('/signUpUser/<Cid>', methods = ['POST'])
def signUpUser(Cid):
    user =  request.values.get('username1', '')
    passw = request.values.get('password1', '')
    data = db.select_username(db,user)
    print(data)
    if data is None:
        db.insert_user(db,user,passw)
        session['logged_in'] = True		
        session['username'] = user
        print("Signed in successfully")
        return render_template('add-contact.html')
    else:
        print("User already excists")
        return render_template('signUp.html')


@app.route('/addContact/<Cid>', methods = ['POST'])
def addContact(Cid):
    print("adding")
    user =  session['username']
    contact = request.values.get('contactname', '')
    data = db.select_contact(db,user,contact)
    data2 = db.select_username(db,contact)
    if data is None:
        if data2 is None:
                print("User does not exist")
                return signUp()
        else:
                db.insert_contact(db,user,contact)
                print("Contact added successfully")
                return render_template('add-contact.html')
    else:
        print("Contact already excists")
        return render_template('add-contact.html')




@app.route('/connectContact/<Cid>', methods = ['POST'])
def connectContact(Cid):
    print("connecting")
    user =  session['username'] 
    contact = request.values.get('contactname', '')
    data = db.select_contact(db,user,contact)
    if data is None:
        print("contact not found")
        return render_template('add-contact.html')
    else:
        print("Contact found")
        uid,_,_=data
        db.insert_awaitingUser(db,user,contact)
        sse.publish({"message": 'connection with id: '+str(uid)+' from :' + user }, type='chatroom', channel='r')
        agent = str(request.user_agent)
        print("Connnection req sent")
        return render_template('add-contact.html')


@app.route('/acceptConnection/<Cid>', methods = ['POST'])
def accept(Cid):
    print("accepting")
    user =  session['username'] 
    contact = request.values.get('contactname', '')
    data = db.select_awaitingUser(db,contact,user)
    if data is None:
        print("no req from contact")
        return render_template('add-contact.html')
    db.delete_awaitingUser(db,contact,user)
    sse.publish({"message": 'accept' + contact}, type='accept', channel='sss')
    agent = str(request.user_agent)
    print("accepted")
    return render_template('add-contact.html')


@app.route('/enterChatRoom')
def enter():
    #print('111111111111111111111111111111111111111111111')
    agent = str(request.user_agent)
    #print(agent)
    return render_template('add-contact.html')


@app.route("/logout/<Cid>", methods = ['POST'])
def logOut(Cid):
	print("logging out")
	session['logged_in'] = False
	session['username'] = 'none'
	return render_template('signUp.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=4000,debug=True)

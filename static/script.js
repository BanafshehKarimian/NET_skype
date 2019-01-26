var uname;
function login(){
	var x = new XMLHttpRequest();
	var data = new FormData();
  	data.append('username', document.getElementById("username").value)
    uname = document.getElementById("username").value
	data.append('password', document.getElementById("password").value)
	x.open('POST', '/logInUser/'+document.getElementById("username").value,true)
  	x.send(data)
}

function signup(){
	var x = new XMLHttpRequest();
	var data = new FormData()
  	data.append('username1', document.getElementById("username1").value)
    uname = document.getElementById("username1").value
	data.append('password1', document.getElementById("password1").value)
	x.open('POST', '/signUpUser/'+document.getElementById("username").value,true)
  	x.send(data)
}


function addContact(){
	var x = new XMLHttpRequest();
	var data = new FormData()
  	data.append('contactname', document.getElementById("contatname").value)
	x.open('POST', '/addContact/'+document.getElementById("username").value,true)
  	x.send(data)
}


function logOut(){
	
	var x = new XMLHttpRequest();
	x.open('POST', '/logout/'+document.getElementById("username").value,true)
  	x.send('logout')
}
function connectContact(){
	var x = new XMLHttpRequest();
	var data = new FormData()
  	data.append('contactname', document.getElementById("contatname1").value)
	x.open('POST', '/connectContact/'+document.getElementById("username").value,true)
    //var hname= window.location.hostname
    //window.open("http:127.0.0.1:5000/user2/3")//////////////////////////////////////window.location.hostname
  	x.send(data)
console.log('request');
   window.location= "http://"+window.location.hostname+":5000/"+document.getElementById("username").value+"/"+document.getElementById("room_id1").value

}

function acceptContact(){
	var x = new XMLHttpRequest();
	var data = new FormData()
  	data.append('contactname', document.getElementById("contatname2").value)
	x.open('POST', '/acceptConnection/'+document.getElementById("username").value,true)
  	x.send(data)
console.log('accept');
	window.location= "http://"+window.location.hostname+":5000/"+document.getElementById("username").value+"/"+document.getElementById("room_id2").value
	var z = 10
}


function redirecting(){
	var x = new XMLHttpRequest();
	var data = new FormData()
  	data.append('contactname', '')
	x.open('POST', '/enterChatRoom')
  	x.send(data)
}

var rm = new EventSource("/stream?channel=r/"+document.getElementById("username").value);
rm.addEventListener('chatroom', function(event) {
    var data = JSON.parse(event.data);
    alert(data.message);
}, false);

var acc = new EventSource("/stream?channel=sss/"+document.getElementById("username").value);
acc.addEventListener('accept', function(event) {
    var data = JSON.parse(event.data);
    //alert(data.message);
    redirecting();
}, false);



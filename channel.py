from flask import Flask
from flask import Blueprint
from flask import request
from flask_sse import sse

channel = Blueprint('channel', __name__)



@channel.route("/send/<channel_name>/<massage_type>", methods=['POST'])
def send(channel_name, massage_type):
    print("sending...!")
    sse.publish({"message": request.data.decode("utf-8")}, type=massage_type, channel=channel_name)
    return "send"+massage_type+"to"+channel_name

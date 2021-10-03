# Flask app (backend) to take UDP message and then send over SocketIO, which React App can read from

from flask import Flask, jsonify
from flask_socketio import SocketIO, emit

#mongo engine for downloading to mongodb
# from pymongo import MongoClient


import socket
import json
import re

## Here we define the UDP IP address as well as the port number that we have
## already defined in the client python script.
UDP_IP = "127.0.0.1"
UDP_PORT = 5000


app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet',  cors_allowed_origins="*")



import eventlet
eventlet.monkey_patch()

## declare our serverSocket upon which
## we will be listening for UDP messages
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
## One difference is that we will have to bind our declared IP address
## and port number to our newly declared serverSock
serverSock.bind((UDP_IP, UDP_PORT))



# @app.route('/', methods=['PUT'])
# def update_record(document):
#     print("sent to mongodb")
#     return jsonify(document)

#configuring mongodb running on docker image
# app.config['MONGODB_SETTINGS'] = {
#     'db': 'test',
#     'host': 'localhost',
#     'port': 27017 ,
#     'username':'admin',
#     'password':'pass'
# }

# client = MongoClient('localhost:27017', username='admin', password='pass', authSource='mongo-dev')
# db = client['test']
# coll = db['delete_me']
# client = MongoClient('localhost:27017')
# client.reporting.authenticate('admin','pass', mechanism='MONGODB-CR')
#needed eventlet to get it working - investigate further

def readFromUDP():
    while True:
        data, addr = serverSock.recvfrom(1024)
        # print ("Received Message: " + str(data))
        data = data.decode("utf-8")
        #print(type(data))
        #print(data)
        p = re.compile('(?<!\\\\)\'')
        data = p.sub('\"', data)
        # data = data.replace("\'", "\"")


        #print(data)
        jsonDocument = json.loads(data)
        socketio.emit("data", {'data': jsonDocument})
        # update_record({'data': jsonDocument})

        # x = coll.insert_one({'data': str(jsonDocument)})
        # db.

        # print("emitted")
    serverSock.close()


@socketio.on("client_connected")
def client_connected(data):
    print("connected~")
    print(str(data))


@socketio.on("connected")
def connected():
    print("connected")


@socketio.on("disconnected")
def disconnected():
    print("disconnected")



if __name__ == "__main__":
    #use to run background function
    socketio.start_background_task(target=readFromUDP)
    print("backgound app started")
    socketio.run(app, port=5001)
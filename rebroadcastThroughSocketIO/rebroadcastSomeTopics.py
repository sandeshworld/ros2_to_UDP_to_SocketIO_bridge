# MIT LICENSE - ALL PURPOSE
# DEVELOPED BY SANDESH BANSKOTA (Github: sandeshworld)
# MODIFY AND USE THIS CODE AS NEEDED, THOUGH KEEP THIS COMMENT

import rclpy
from rclpy.node import MsgType, Node

# tried the following

# import socketio
# from aiohttp import web
# import eventlet
# import threading
# import requests

import socket


# -------------------------------------------------------------------------------------

# TODO: import the msg type you would like to rebroadcast here

from std_msgs.msg import String
from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import Imu

#topic used to control vehicle - make sure to install these messages to use them
from lgsvl_msgs.msg import VehicleControlData
from lgsvl_msgs.msg import CanBusData

# ------------------------------------------------------------------------------------

#import from the other file
# from scanProcessor import *
import indyRacePack.scanProcessor as sp

# code to modularize conversion of msg to JSON
def msgToJson(msgType, data):
    
    jsonDocument = {}

    fields = CanBusData.get_fields_and_field_types();
    
    for key in fields.keys():
        # get attr converts string to attribute
        jsonDocument[key] = getattr(data, key)

    print(jsonDocument)
    return jsonDocument


UDP_IP = "127.0.0.1"
UDP_PORT = 5000
# this class will subscribe to the lidar topic and then publish
# to the vehicle control publisher to maintain follow following going around the track
class RebroadcastSomeTopics(Node):

    def __init__(self):
        super().__init__('republishOverSocketIO')

        self.sock = socket.socket(socket.AF_INET, # Internet 
                                socket.SOCK_DGRAM) # UDP
        print("port connected ")


        # TODO: create subscription here as needed

        # self.subscription_lidar_front = self.create_subscription(
        #     PointCloud2,
        #     'lidar_front/points_raw',
        #     self.lidar_front_callback,
        #     10)

        # self.subscription_imu = self.create_subscription(
        #     Imu,
        #     '/imu/imu_raw',
        #     self.imu_callback,
        #     10
        # )

        self.subscription_state_data = self.create_subscription(
            CanBusData,
            '/lgsvl/state_report',
            self.state_report_callback,
            10
        )
        
        # self.subscription_lidar_front # prevent unused variable warning
        # self.subscription_imu
        self.subscription_state_data


    # def lidar_front_callback(self, data):
    #     #distanceFromWall = self.returnDistance(data)
    #     cloud_points = list(sp.read_points(data, skip_nans=True, field_names = ("x", "y", "z")))
    #     print(cloud_points[0])
    #     # self.sio.emit('lidar event', str(cloud_points))
    #     # x = requests.post('ws://localhost:5000', data = str(cloud_points))
    #     self.sock.sendto(str(cloud_points).encode('utf-8'), (UDP_IP, UDP_PORT))

    def imu_callback(self, data):
        imu_data = data
        print(imu_data)
        # x = requests.post('ws://localhost:5000', data = str(imu_data))
        self.sock.sendto((str(imu_data).encode('utf-8')), (UDP_IP, UDP_PORT))

    def state_report_callback(self, data):
        document = msgToJson(CanBusData, data)
        document.pop('header')
        for key in document.keys():
            document[key] = str(document[key])
        # document['orientation'] = str(document['orientation'])
        # document['linear_velocities'] = str(document['linear_velocities'])
        self.sock.sendto((str(document).encode('utf-8')), (UDP_IP, UDP_PORT))


def main(args=None):
    rclpy.init(args=args)

    rebroadcaster = RebroadcastSomeTopics()

    # x = threading.Thread(target=rclpy.spin_once, args=(rebroadcaster,))
    rclpy.spin(rebroadcaster)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    rebroadcaster.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()


# i tried multithreading to get socketio and ros.spin working at same time.
# there was issue with deadlock

# Post, but post requires an ack which could keep things hanging

# i.e.
        # timer_period = 0.5  # seconds

        # initialize socketio stuff
        # self.sio = socketio.Server()
        # # wrap with a WSGI application
        # self.app = socketio.WSGIApp(self.sio)

        # eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

        # sio.connect('ws://localhost:9001')
        # self.sio.connect('ws://localhost:5000')
import paho.mqtt.client as mqtt
import json
import os
THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = '1IS17pD9oFvcEE6G4O5W'
rb = ''
def on_connect(client, userdata, rc, *extra_params):
    print("Connected with result code "+str(rc))
    client.subscribe('v1/devices/me/rpc/request/+')
def on_message(client, userdata, msg):
    print(msg.topic)
    print(msg.payload)
    payload = msg.payload.decode()
    data_sensor = json.loads(payload)
    rb = data_sensor['params']
    rb = str (rb)
    print(rb) 
    print(type(rb))
    if ( rb == 'True' ) :
 	print('1')
	os.system('reboot')
if __name__ == "__main__":
   client = mqtt.Client()
   client.username_pw_set(ACCESS_TOKEN)
   client.connect(THINGSBOARD_HOST, 1883)
   client.loop_start()
   while True :
   		 client.on_connect = on_connect
   		 client.on_message = on_message
		   
   client.disconect()
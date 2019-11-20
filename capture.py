import cv2
import time
import numpy as np
import firebase_admin
import paho.mqtt.client as mqtt
import json
import time
import datetime
from firebase_admin import credentials
from firebase_admin import storage

rtsp_domain = "rtsp://admin:88888888abc@192.168.0.102:554/Streaming/Channels/101"

THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 's9vGSLI2VyxmNL3Ehl7e'
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()
status = {'Status' : ''}

try:
    cap = cv2.VideoCapture(rtsp_domain)
    count = 0
    while not cap.isOpened():
        cap = cv2.VideoCapture(rtsp_domain)
        count = count + 1
        if count == 50:
            break
except IOError : 
    message = 'Cant connect to camera'
    status['Status'] = 'Cant connect to camera'
    client.publish('v1/devices/me/telemetry',json.dumps(status),1)
else:
    if cap.isOpened():
        ret , frame = cap.read()
	tm = time.asctime(time.localtime(time.time()))
	filename = 'capture/'+str(tm) +'.jpg' 
	cv2.imwrite(filename,frame)
	try:
	    cred = credentials.Certificate('nct-algri-firebase-adminsdk-x0852-0235c1cbc9.json')
	    firebase_admin.initialize_app(cred, {
    		'storageBucket': 'nct-algri.appspot.com'
			})

	    bucket = storage.bucket()

	    blob = bucket.blob(filename)
	    blob.upload_from_filename(filename)
	except:
	    message = 'Cant connect to cloud'
	    status['Status'] = 'Cant connect to cloud'
	    client.publish('v1/devices/me/telemetry',json.dumps(status),1)
	else:
	    message = "Successful"
	    status['Status'] = 'Send images succesful'
	    client.publish('v1/devices/me/telemetry',json.dumps(status),1)
    else:
        message = 'Cant connect camera'
	status['Status'] = 'Cant connect camera'
	client.publish('v1/devices/me/telemetry',json.dumps(status),1)
finally:
    cap.release()
    print(message)
    cv2.destroyAllWindows()
    with open ('log.txt',"a") as logfile:
        t = time.asctime(time.localtime(time.time()))
        logfile.write(t+" "+message+'\n')
        logfile.close()

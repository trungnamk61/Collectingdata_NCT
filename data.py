import serial 
import mysql.connector
import paho.mqtt.client as mqtt
import datetime
import json
import time

temp= []
watertemp = []
humi = []
ec = []
ph = []
lux = []
status = {'status' : ''}

def database() :
    mydb = mysql.connector.connect(
    host="us-cdbr-iron-east-02.cleardb.net",
    user="b801f230629d30",
    passwd="91690179",
    database="heroku_c56b50141fa0f31"
    )
   
    mydb.close()

def getdata():
    global  date 
    global  count_t 
    global  count_h
    global  count_e 
    global  count_p 
    global  count_l 
    global  count_wt
    global count
    a  = serialfromarduino.readline() 
    file.write(a)
    a=a.decode()
    a=a.rstrip()
    b = serialfromarduino.readline() 
    c = b
    b=b.rstrip()
    b=float(b)
    if (a == 'Temperature') :
        count_t=b 
        temp.append(b)
        print ("Temp:")
        print (temp)
        #count=count+1
        file.write(c)
    if (a == 'WaterTemperature') :
        count_wt=b  
        watertemp.append(b)
        print ("Water temp:")
        print (watertemp)
        #count=count+1
        file.write(c)
    if (a == 'Humidity') : 
        count_h=b 
        humi.append(b)
        print ("Humi:")
        print (humi)
        #count=count+1
        file.write(c)
    if (a == 'EC') : 
        count_e=b 
        ec.append(b)
        print ("EC:")
        print (ec)
        #count=count+1
        file.write(c)
    if (a == 'pH') : 
        count_p=b 
        ph.append(b)
        print ("pH:")
        print (ph)
        #count=count+1
        file.write(c)
    if (a == 'LightIntensity') : 
        count_l=b 
        lux.append(b)
        print ("Light Intensity:")
        print (lux)
        #count=count+1
        file.write(c)
        date = datetime.datetime.now()
        date = str(date)
        print (date)
        file.write(date+'\n') 
        mydb = mysql.connector.connect(
    	host="us-cdbr-iron-east-02.cleardb.net",
    	user="b801f230629d30",
    	passwd="91690179",
    	database="heroku_c56b50141fa0f31"
    	)
        mycursor = mydb.cursor()
        sql = "INSERT INTO data_nct (temp,humi,lux,pH,ec,water_temp,timestamp) value (%s,%s,%s,%s,%s,%s,%s)"  
        val = (count_t,count_h,count_l,count_p,count_e,count_wt,date)
        mycursor.execute(sql,val)
        mydb.commit()
	mydb.close()
        if (count_t == 0.000 or count_h ==0 ) :
            status['Status'] = 'DHT22 is not active'
            client.publish('v1/devices/me/telemetry',json.dumps(status),1)
            time.sleep(1)
        if (count_l == -1.000 or count_l == 0.000):
            status['Status'] = 'BH1750 is not active'
            client.publish('v1/devices/me/telemetry',json.dumps(status),1)
            time.sleep(1)
        if( count_wt == 0.000) :
            status['Status'] = 'Sensor water is not active'
            client.publish('v1/devices/me/telemetry',json.dumps(status),1)
            time.sleep(1)
        if ( count_e == 0.000) :
            status['Status'] = 'EC is not active'
            client.publish('v1/devices/me/telemetry',json.dumps(status),1)
            time.sleep(1)
        if (count_p <=13.350 and count_p >= 13.270) :
            status['Status'] = 'pH is not active'
            client.publish('v1/devices/me/telemetry',json.dumps(status),1)
            time.sleep(1)
        if (count_t > 0 and count_h > 0 and count_l > 0 and count_e > 0 and  count_p <13.270 and count_wt > 0):
            status['Status'] = 'Sensor is active'
            client.publish('v1/devices/me/telemetry',json.dumps(status),1)
            time.sleep(1)
	count=count+1
	print(count)
    file.seek(0,2)
def main():
    global  date 
    global  count_t 
    global  count_h
    global  count_e 
    global  count_p 
    global  count_l 
    global  count_wt
    global  count 
    global serialfromarduino
    global client
    global file
    global count_network
    global count 
    count_network = 0
    count = 0
    THINGSBOARD_HOST = 'demo.thingsboard.io'
    ACCESS_TOKEN = 'Y3wJ8SUkSDe2CIdXKWdu'
    #thingsboard configure
    client = mqtt.Client()
    client.username_pw_set(ACCESS_TOKEN)
    client.connect(THINGSBOARD_HOST, 1883, 60)
    client.loop_start()

    #USB configure
    port = "/dev/ttyUSB0"
    serialfromarduino = serial.Serial(port,115200)  
    file = open ("data.txt","a+")
    while True:
     	if(serialfromarduino.inWaiting()>0) : 
		try:
      			client.connect(THINGSBOARD_HOST, 1883, 60)
		except :
			if ( count_network == 50 ) :
				client.loop_stop()
   				client.disconnect()   
    				file.close()
				quit()
	 		print("MQTT disconnect when get data! ")
			count_network = count_network + 1 
			time.sleep(5)
		else :
			try :
				mydb = mysql.connector.connect(
    				host="us-cdbr-iron-east-02.cleardb.net",
    				user="b801f230629d30",
    				passwd="91690179",
    				database="heroku_c56b50141fa0f31"
    				)
			except :
				if ( count_network == 50 ) :
					client.loop_stop()
   					client.disconnect()   
    					file.close()
					quit()
				print("Database disconnect when get data!!!")
				count_network = count_network + 1 
				time.sleep(5)
			else :  
				print("Internet connected !!!")
       				getdata()		
				if ( count == 6 ) :
					client.loop_stop()
   					client.disconnect()   
    					file.close()
					quit()
    client.loop_stop()
    client.disconnect()   
    file.close()

THINGSBOARD_HOST = 'demo.thingsboard.io' 
ACCESS_TOKEN = 'Y3wJ8SUkSDe2CIdXKWdu'
port = "/dev/ttyUSB0"
while True :
    time.sleep(10)
    try :
      file = open ("data.txt","a+")
      file.close
    except KeyboardInterrupt :
      del temp,watertemp,humi,ec,ph,lux,status 
      del date,count_t,count_h,count_e,count_p,count_l,count_wt,serialfromarduino,client,file
    except :
      print("File doesn't open !")
    else : 
      try :
		port = "/dev/ttyUSB0"
		serialfromarduino = serial.Serial(port,115200) 
      except :
		print("Serial port disconnect ! ")
      else :
		try:
      			client = mqtt.Client()
      			client.username_pw_set(ACCESS_TOKEN)
      			client.connect(THINGSBOARD_HOST, 1883, 60)
			#client.disconnect()
		except :
	 		print("MQTT disconnect ! ")
		else :
			try :
				mydb = mysql.connector.connect(
    				host="us-cdbr-iron-east-02.cleardb.net",
    				user="b801f230629d30",
    				passwd="91690179",
    				database="heroku_c56b50141fa0f31"
    				)
				mydb.close()
			except :
				print("Database disconnect !!!")
			else :  
				print("Internet connected !!!")
      				main()
				
    #second = time.time()
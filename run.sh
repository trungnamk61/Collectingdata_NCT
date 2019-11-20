count=0
while :
do
	if [ "$(date +'%M')" = "00" ]
	then
		echo "Capture Image !!!"
		python /home/pi/NCT/Collectingdata_NCT/capture.py
		sleep 3
		echo "Get data from ESP32"
		python /home/pi/NCT/Collectingdata_NCT/data.py
		let "count++"
		echo $count
	fi
	wait
		if [ "$count" = "1" ]
		then
			break
		fi
done 

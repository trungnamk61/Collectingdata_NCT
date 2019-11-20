while :
do 
	python /home/pi/NCT/Collectingdata_NCT/reboot.py &
	sh /home/pi/NCT/Collectingdata_NCT/run.sh &
	wait
done
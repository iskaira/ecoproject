import subprocess
import threading
from time import sleep
from threading import Thread
import RPi.GPIO as GPIO
import constants
import firebase

#from Subfact_ina219 import INA219

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)
state=1
vcc=1
firebase = firebase.FirebaseApplication('https://ecolamp-c8fda.firebaseio.com/', None)
_on=True
_run=False
_bat=False

#ina = INA219()

def get_firebase():
	global state
	global vcc
	sleep(1)
	while _on:
		result = firebase.get('/Lamp', None)
		state=result['state']
		vcc = result['vcc']

#38 PIN - SVET
#40 PIN - VCC
#print state
#print vcc
'''
def Auto_energy():
	global _bat
	while _bat:
		print ("Bus     : %.3f V" % ina.getBusVoltage_V())
		print ("Current : %.3f mA" % ina.getCurrent_mA())
		print ("WATT    : %.3f mW" % ina.getPower_mW())
		
		if ina.getBusVoltage_V()<=11.8:#220V
			GPIO.output(40,GPIO.LOW)
		elif ina.getBusVoltage_V()>12.5 : #12V
			GPIO.output(40,GPIO.HIGH)
			#REL'e FOR NOT COLLECTING ENERGY FROM SOLAR PANEL
		sleep(30)
'''
def running():		
	global _run
	global GPIO
	global threadA
	global state
	global _bat
	global vcc
	
	sleep(0.5)
	while True:
		print(state)
		print(vcc)	
		if state==0:
			print("AUTO MODE ON")
			_run=True
		else:
			_run=False
			print ("AUTO MODE OFF")
			if state==1:
				print ('Lights On')
				GPIO.output(38,GPIO.LOW)# na 40 HIGH
				#GPIO.output(40,GPIO.LOW)
			if state==2:
				print ('Lights Off')
				GPIO.output(38,GPIO.HIGH) # na 40 LOW


		if vcc==1:
			print ('always 220v')
			GPIO.output(40,GPIO.LOW)
		if vcc==0:
			print ('battery check mode')
			_bat=True
			'''
			if not threadA.isAlive():
				threadA = Thread(target = Auto_energy)
				threadA.start()
				GPIO.output(38,GPIO.LOW)
				GPIO.output(40,GPIO.HIGH)
			'''
		sleep(2)
	
#threadA = Thread(target = Auto_energy)

threadB = Thread(target = running)
threadD = Thread(target = get_firebase)
threadB.setDaemon = True
threadD.setDaemon = True
threadB.start()
threadD.start()
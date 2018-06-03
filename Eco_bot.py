import telebot
import constants

import subprocess
import threading
from time import sleep
from threading import Thread
from multiprocessing import Process
from firebase import firebase

bot = telebot.TeleBot(constants.token)
firebase = firebase.FirebaseApplication('https://ecolamp-c8fda.firebaseio.com/', None)
print(firebase)
'''
state:
0-auto
1-on
2-off
vcc:
0-auto
1-auto_off
'''
automatic =u"\U0001F916"+'Autonomous Mode'	
battery = u"\U0001F50B" + 'Eco Mode ON'
V220=	u"\U0001F50C" + 'Eco Mode OFF'	
#statistics ='\xF0\x9F\x93\x88'+'Statistics'
on=u"\U0001F31D" + 'Lights ON'	
off=u"\U0001F31A" + 'Lights OFF'			
@bot.message_handler(commands=['start'])
def rp(message):
	markup = telebot.types.ReplyKeyboardMarkup(True,False)
	markup.row(on,off)
	markup.row(battery,V220)
	markup.row(automatic)
	bot.send_message(message.from_user.id,'Hello, this is beta version of Eco Lamp Bot, we will help you to control your Energy wisely!',reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
	markup = telebot.types.ReplyKeyboardMarkup(True,False)
	markup.row(on,off)
	markup.row(battery,V220)
	markup.row(automatic)
	bot.send_message(message.from_user.id,'1 - Automatic mode is used to make your lamp be controlled via bot.\n2 - When you switch to ~Light on/off~ commands, automatic mode will be down!',reply_markup=markup)

@bot.message_handler(content_types=['text'])
def message(message):
	global markup
	print (message.text)
	markup = telebot.types.ReplyKeyboardMarkup(True,False)
	markup.row(on,off)
	markup.row(battery,V220)
	markup.row(automatic)#,statistics)
	if message.text==automatic:	
		bot.send_message(message.from_user.id,'Set Autonomous Mode ON...',reply_markup=markup)
		firebase.put('/Lamp','state',0) #State - 0  Autonomous
	if message.text==on:
		firebase.put('/Lamp','state',2)#Change 1
		bot.send_message(message.from_user.id,'Lights On',reply_markup=markup)
		print ('Autonomous mode off && Lights On'	)
	if message.text==off:
		print ('Autonomous mode off && Lights off')
		firebase.put('/Lamp','state',1)#Change2
		bot.send_message(message.from_user.id,'Lights Off',reply_markup=markup)
	
	if message.text==V220:
		bot.send_message(message.from_user.id,'Eco Mode Off',reply_markup=markup)
		print ('220v Eco mode Off')
		firebase.put('/Lamp','vcc',1)
	if message.text==battery:
		print ('Eco Mode On')
		bot.send_message(message.from_user.id,'Eco Mode On',reply_markup=markup)
		firebase.put('/Lamp','vcc',0)

	sleep(0.3)

if '__main__' == __name__:
	bot.polling(none_stop=True)
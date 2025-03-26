from pyfirmata import Arduino, util, STRING_DATA
from time import sleep
import telebot

comport='COM10'

board=Arduino(comport)
sleep(1.5)

telToken = '6761087563:AAEKOLyToOpRb_zwjPZn9eHsdSJt8iyFrUc'
chatID = '-1001994273832'

led_1=board.get_pin('d:12:o')
pirPin = board.get_pin('a:1:i')
hujanPin = board.get_pin('a:2:i')
asapPin = board.get_pin('a:3:i')
buzzerPin = 11

it = util.Iterator(board)
it.start()

SmartHomeBot = telebot.TeleBot(telToken) 

def sendTelMessage(message):
    SmartHomeBot.send_message(chat_id=chatID, text=message)

def alarmAnnou(pin, msg):
    print(msg)
    sendTelMessage(msg)
    board.digital[pin].write(1)
    sleep(0.5)
    board.digital[pin].write(0)
    sleep(0)

def led(total):
    if total==0:
        led_1.write(0)
        sendTelMessage("Status: Relay Mati")
    elif total==1:
        led_1.write(1)
        sendTelMessage("Status: Relay 1 Menyala")

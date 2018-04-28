#! /usr/bin/python
# R.O.B. Desktop Notification Assistant
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, commands, subprocess, re, json, sys, os
from random import randint
from gpiozero import Button
from datetime import datetime
import RPi.GPIO as GPIO
import includes.settings as settings
import includes.data as data
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

# setup LEDs by GPIO pins / buttons and turn off the lights
BLUE = 17
YELLOW = 13
GREEN = 6
RED = 12
GPIO.setup(BLUE,GPIO.OUT)
GPIO.setup(YELLOW,GPIO.OUT)
GPIO.setup(GREEN,GPIO.OUT)
GPIO.setup(RED,GPIO.OUT)
redButton = Button(16)
blueButton = Button(26)

# begin default display text and button listeners
subprocess.call(["/home/pi/RobbieAssistant/digole", "setRot90"])
subprocess.call(["/home/pi/RobbieAssistant/digole", "clear"])
subprocess.call(["/home/pi/RobbieAssistant/digole", "setColor", "255"])

def randomTitleScreen():
    '''show NES game title screen on the Digole Display
    @titleScreenNumber : number 1 to 20 of which title screen to show
    '''

    # clear the previous title screen
    isUpdatingTitle = True
    subprocess.call(["/home/pi/RobbieAssistant/digole", "ClearTitle"])
    subprocess.call(["/home/pi/RobbieAssistant/digole", "NES"])

    # show one of 20 titles
    titleScreenNumber = randint(1,20)
    if titleScreenNumber == 1:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "BlasterMaster"])
    if titleScreenNumber == 2:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "Castlevania"])
    if titleScreenNumber == 3:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "ChipDale"])
    if titleScreenNumber == 4:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "Contra"])
    if titleScreenNumber == 5:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "DuckTales"])
    if titleScreenNumber == 6:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "Galaga"])
    if titleScreenNumber == 7:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "GhostBusters"])
    if titleScreenNumber == 8:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "Gradius"])
    if titleScreenNumber == 9:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "KidIcarus"])
    if titleScreenNumber == 10:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "MarbleMadness"])
    if titleScreenNumber == 11:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "MegaMan"])
    if titleScreenNumber == 12:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "MetalGear"])
    if titleScreenNumber == 13:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "Metroid"])
    if titleScreenNumber == 14:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "PunchOut"])
    if titleScreenNumber == 15:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "SuperMario2"])
    if titleScreenNumber == 16:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "SuperMario3"])
    if titleScreenNumber == 17:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "TMNT2"])
    if titleScreenNumber == 18:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "TopGun"])
    if titleScreenNumber == 19:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "Turtles"])
    if titleScreenNumber == 20:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "Zelda"])
    isUpdatingTitle = False

def resetLights():
    '''THERE...ARE... FOUR LIGHTS!'''
    GPIO.output(BLUE,GPIO.LOW)
    GPIO.output(YELLOW,GPIO.LOW)
    GPIO.output(GREEN,GPIO.LOW)
    GPIO.output(RED,GPIO.LOW)

previousMessage = ''
def showMessage(message):
    '''show messages on screen, making the original message black first'''
    global previousMessage
    subprocess.call(["/home/pi/RobbieAssistant/digole", "setFont", "51"])
    subprocess.call(["/home/pi/RobbieAssistant/digole", "setColor", "0"])
    subprocess.call(["/home/pi/RobbieAssistant/digole", "printxy_abs", "0", "150", previousMessage])
    subprocess.call(["/home/pi/RobbieAssistant/digole", "setColor", "255"])
    subprocess.call(["/home/pi/RobbieAssistant/digole", "printxy_abs", "0", "150", message])
    previousMessage = message
    
previousMessageCount = ''
def showUnreadMessageCount(count):
    '''show how many messages unread'''
    global previousMessageCount
    messageCount = str(count) + " unread"
    subprocess.call(["/home/pi/RobbieAssistant/digole", "setFont", "18"])
    subprocess.call(["/home/pi/RobbieAssistant/digole", "setColor", "0"])
    subprocess.call(["/home/pi/RobbieAssistant/digole", "printxy_abs", "220", "210", previousMessageCount])
    resetLights()
    if count > 0:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "setColor", "250"])
        GPIO.output(RED,GPIO.HIGH)
    else:
        subprocess.call(["/home/pi/RobbieAssistant/digole", "setColor", "222"])
        GPIO.output(GREEN,GPIO.HIGH)
    subprocess.call(["/home/pi/RobbieAssistant/digole", "printxy_abs", "220", "210", messageCount])
    previousMessageCount = messageCount

def logMessageToFile(currentMessage):
    '''log messages to file for later reference'''
    file = open("/home/pi/RobbieAssistant/logs/notifications.log","a")
    file.write("\n" + currentMessage)

previousTime = ''
previousIndoorTemp = ''
previousOutdoorTemp = ''
def showTimeWeather():
    '''show time and weather'''
    global previousTime, previousIndoorTemp, previousOutdoorTemp
    
    # update time and weather
    now = datetime.now()
    tempInfo = data.getJSONFromDataFile('temp.data')
    weatherInfo = data.getJSONFromDataFile('weather.data')     
    
    if tempInfo != '' and weatherInfo != '':
        time = now.strftime("%I:%M")
        indoorTemp = data.convertToString(data.convertToInt(tempInfo['temp'])) + "*F"
        outdoorTemp = data.convertToString(data.convertToInt(weatherInfo['apparentTemperature'])) + "*F"
        
        subprocess.call(["/home/pi/RobbieAssistant/digole", "setFont", "123"])

        subprocess.call(["/home/pi/RobbieAssistant/digole", "setColor", "0"])
        subprocess.call(["/home/pi/RobbieAssistant/digole", "printxy_abs", "170", "50", previousTime])    
        subprocess.call(["/home/pi/RobbieAssistant/digole", "setColor", "255"])
        subprocess.call(["/home/pi/RobbieAssistant/digole", "printxy_abs", "170", "50", time])
        
        subprocess.call(["/home/pi/RobbieAssistant/digole", "setFont", "120"])

        subprocess.call(["/home/pi/RobbieAssistant/digole", "setColor", "0"])
        subprocess.call(["/home/pi/RobbieAssistant/digole", "printxy_abs", "150", "90", previousIndoorTemp])
        subprocess.call(["/home/pi/RobbieAssistant/digole", "setColor", "254"])
        subprocess.call(["/home/pi/RobbieAssistant/digole", "printxy_abs", "150", "90", indoorTemp])
        
        subprocess.call(["/home/pi/RobbieAssistant/digole", "setColor", "255"])
        subprocess.call(["/home/pi/RobbieAssistant/digole", "printxy_abs", "218", "90", "/"])
        
        subprocess.call(["/home/pi/RobbieAssistant/digole", "setColor", "0"])
        subprocess.call(["/home/pi/RobbieAssistant/digole", "printxy_abs", "240", "90", previousOutdoorTemp])
        subprocess.call(["/home/pi/RobbieAssistant/digole", "setColor", "223"])
        subprocess.call(["/home/pi/RobbieAssistant/digole", "printxy_abs", "240", "90", outdoorTemp])
        
        previousTime = time
        previousIndoorTemp = indoorTemp
        previousOutdoorTemp = outdoorTemp

def scrollOldMessages():
    '''scroll through old messages'''
    global oldMessageShown, showPreviousMessageTimeout, checkForMessageTimeout, isUpdatingTitle
    
    # ignore if we're updating the title screen
    if isUpdatingTitle:
        return False
    
    # set the times back to zero because now you're scrolling through old messages
    showPreviousMessageTimeout = 0
    checkForMessageTimeout = 0
    
    # show previous message based on where you are in the history
    with open("logs/notifications.log") as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        content.reverse()
        message = content[oldMessageShown]
    previousMessage = message
    showMessage(message)
    oldMessageShown = oldMessageShown + 1

def clearUnread():
    '''clear unread messages flag'''
    global unreadMessageCount, oldMessageShown, clearButtonPressedMessage, isUpdatingTitle
    
    # ignore if we're updating the title screen
    if isUpdatingTitle:
        return False
    
    # clear current message and unread count, user acknowledged message activity
    oldMessageShown = 0
    unreadMessageCount = 0
    clearButtonPressedMessage = message
    showMessage('')
    showUnreadMessageCount(unreadMessageCount)
    
# set variable defaults
message = ''
maxMessageLength = 48
previousMessage = 'Hello! This is R.O.B.'
unreadMessageCount = 0
oldMessageShown = 0
clearButtonPressedMessage = ''
isUpdatingTitle = False

# timeout values
checkForMessageTimeout = 0
rotateTitleTimeout = 0

# setup the display
resetLights()
randomTitleScreen()
showTimeWeather()

# start Robbie!
while True:
    redButton.when_pressed = clearUnread
    blueButton.when_pressed = scrollOldMessages

    # check for new messages
    checkForMessageTimeout = checkForMessageTimeout + 1
    if checkForMessageTimeout > 10000:
        incomingMessage = json.loads(unicode(subprocess.check_output(['curl', "http://" + settings.dashboardServer + "/message"]), errors='ignore'))
        message = str(incomingMessage["message"])
        message = message[:maxMessageLength]
        
        # if new message then show it as long as the previous message wasn't cleared out by the clear button press
        if (previousMessage != message) and (clearButtonPressedMessage != message):
            logMessageToFile(message)
            showMessage(message)
            unreadMessageCount = unreadMessageCount + 1
            showUnreadMessageCount(unreadMessageCount)
        checkForMessageTimeout = 0

    # rotate the title screen shown and time / weather
    rotateTitleTimeout = rotateTitleTimeout + 1
    if rotateTitleTimeout > 60000:
        randomTitleScreen()
        showTimeWeather()
        rotateTitleTimeout = 0    

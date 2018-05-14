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

# digole local executable for display and log file location
digoleCommand = "/home/pi/RobbieAssistant/digole"
notificationsLogFile = "/home/pi/RobbieAssistant/logs/notifications.log"

# begin default display text and button listeners
subprocess.call([digoleCommand, "setRot90"])
subprocess.call([digoleCommand, "clear"])
subprocess.call([digoleCommand, "setColor", "255"])

def randomTitleScreen():
    '''show NES game title screen on the Digole Display
    @titleScreenNumber : number 1 to 20 of which title screen to show
    '''

    # clear the previous title screen
    isUpdatingTitle = True
    subprocess.call([digoleCommand, "ClearTitle"])
    subprocess.call([digoleCommand, "NES"])

    # show one of 20 titles
    titleScreenNumber = randint(1,20)
    if titleScreenNumber == 1:
        subprocess.call([digoleCommand, "BlasterMaster"])
    if titleScreenNumber == 2:
        subprocess.call([digoleCommand, "Castlevania"])
    if titleScreenNumber == 3:
        subprocess.call([digoleCommand, "ChipDale"])
    if titleScreenNumber == 4:
        subprocess.call([digoleCommand, "Contra"])
    if titleScreenNumber == 5:
        subprocess.call([digoleCommand, "DuckTales"])
    if titleScreenNumber == 6:
        subprocess.call([digoleCommand, "Galaga"])
    if titleScreenNumber == 7:
        subprocess.call([digoleCommand, "GhostBusters"])
    if titleScreenNumber == 8:
        subprocess.call([digoleCommand, "Gradius"])
    if titleScreenNumber == 9:
        subprocess.call([digoleCommand, "KidIcarus"])
    if titleScreenNumber == 10:
        subprocess.call([digoleCommand, "MarbleMadness"])
    if titleScreenNumber == 11:
        subprocess.call([digoleCommand, "MegaMan"])
    if titleScreenNumber == 12:
        subprocess.call([digoleCommand, "MetalGear"])
    if titleScreenNumber == 13:
        subprocess.call([digoleCommand, "Metroid"])
    if titleScreenNumber == 14:
        subprocess.call([digoleCommand, "PunchOut"])
    if titleScreenNumber == 15:
        subprocess.call([digoleCommand, "SuperMario2"])
    if titleScreenNumber == 16:
        subprocess.call([digoleCommand, "SuperMario3"])
    if titleScreenNumber == 17:
        subprocess.call([digoleCommand, "TMNT2"])
    if titleScreenNumber == 18:
        subprocess.call([digoleCommand, "TopGun"])
    if titleScreenNumber == 19:
        subprocess.call([digoleCommand, "Turtles"])
    if titleScreenNumber == 20:
        subprocess.call([digoleCommand, "Zelda"])
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
    subprocess.call([digoleCommand, "setFont", "51"])
    subprocess.call([digoleCommand, "setColor", "0"])
    subprocess.call([digoleCommand, "printxy_abs", "0", "150", '                                                                                            '])
    subprocess.call([digoleCommand, "setColor", "255"])
    subprocess.call([digoleCommand, "printxy_abs", "0", "150", message])
    previousMessage = message
    
previousMessageCount = ''
def showUnreadMessageCount(count):
    '''show how many messages unread'''
    global previousMessageCount
    messageCount = str(count) + " unread"
    subprocess.call([digoleCommand, "setFont", "18"])
    subprocess.call([digoleCommand, "setColor", "0"])
    subprocess.call([digoleCommand, "printxy_abs", "220", "210", previousMessageCount])
    resetLights()
    if count > 0:
        subprocess.call([digoleCommand, "setColor", "250"])
        GPIO.output(RED,GPIO.HIGH)
    else:
        subprocess.call([digoleCommand, "setColor", "222"])
        GPIO.output(GREEN,GPIO.HIGH)
    subprocess.call([digoleCommand, "printxy_abs", "220", "210", messageCount])
    previousMessageCount = messageCount

def logMessageToFile(currentMessage):
    '''log messages to file for later reference'''
    file = open(notificationsLogFile,"a")
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
        
        subprocess.call([digoleCommand, "setFont", "123"])

        subprocess.call([digoleCommand, "setColor", "0"])
        subprocess.call([digoleCommand, "printxy_abs", "170", "50", previousTime])    
        subprocess.call([digoleCommand, "setColor", "255"])
        subprocess.call([digoleCommand, "printxy_abs", "170", "50", time])
        
        subprocess.call([digoleCommand, "setFont", "120"])

        subprocess.call([digoleCommand, "setColor", "0"])
        subprocess.call([digoleCommand, "printxy_abs", "150", "90", previousIndoorTemp])
        subprocess.call([digoleCommand, "setColor", "254"])
        subprocess.call([digoleCommand, "printxy_abs", "150", "90", indoorTemp])
        
        subprocess.call([digoleCommand, "setColor", "255"])
        subprocess.call([digoleCommand, "printxy_abs", "218", "90", "/"])
        
        subprocess.call([digoleCommand, "setColor", "0"])
        subprocess.call([digoleCommand, "printxy_abs", "240", "90", previousOutdoorTemp])
        subprocess.call([digoleCommand, "setColor", "223"])
        subprocess.call([digoleCommand, "printxy_abs", "240", "90", outdoorTemp])
        
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
    with open(notificationsLogFile) as f:
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

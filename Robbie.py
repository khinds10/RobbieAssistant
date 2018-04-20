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

def randomTitleScreen(titleScreenNumber):
    '''show NES game title screen on the Digole Display
    @titleScreenNumber : number 1 to 20 of which title screen to show
    '''
    subprocess.call(["/home/pi/RobbieAssistant/digole", "clear"])
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

def clearDisplay():
    '''set screen back to default'''
    global oldMessageShown
    oldMessageShown = 0
    showTitleScreenTimeDate()
    showMessage(time.strftime(" %a, %b %d\n\n%m/%d/%Y"))

def refreshDisplay():
    '''refresh just the NES title screen and time/date'''
    showTitleScreenTimeDate()

def showTitleScreenTimeDate():
    '''show time and weather conditions'''
    global data
    try:
        randomTitleScreen(randint(1,20))
        now = datetime.now()
        tempInfo = data.getJSONFromDataFile('temp.data')
        weatherInfo = data.getJSONFromDataFile('weather.data')
        subprocess.call(["/home/pi/RobbieAssistant/digole", "setFont", "123"])
        subprocess.call(["/home/pi/RobbieAssistant/digole", "printxy_abs", "170", "50", now.strftime("%I:%M")])
        subprocess.call(["/home/pi/RobbieAssistant/digole", "setFont", "120"])
        subprocess.call(["/home/pi/RobbieAssistant/digole", "printxy_abs", "150", "90", data.convertToString(data.convertToInt(weatherInfo['apparentTemperature'])) + "*F / " + data.convertToString(data.convertToInt(tempInfo['temp'])) + "*F"])
    except:
        pass

def logMessageToFile():
    '''log messages to file for later reference'''
    global currentMessage
    data.appendRawToFile('notifications.log', "\n" + currentMessage)

def showMessage(message):
    '''show messages on screen, making the original message black first'''
    global currentMessage
    subprocess.call(["/home/pi/RobbieAssistant/digole", "setFont", "51"])
    subprocess.call(["/home/pi/RobbieAssistant/digole", "setColor", "0"])
    subprocess.call(["/home/pi/RobbieAssistant/digole", "printxy_abs", "0", "150", currentMessage])
    subprocess.call(["/home/pi/RobbieAssistant/digole", "setColor", "255"])
    subprocess.call(["/home/pi/RobbieAssistant/digole", "printxy_abs", "0", "150", message])
    currentMessage = message

def checkForMessages():
    '''ask the dashboard instance for a new message to show'''
    global recentMessage
    try:
        incomingMessage = json.loads(unicode(subprocess.check_output(['curl', "http://" + settings.dashboardServer + "/message"]), errors='ignore'))
        message = str(incomingMessage["message"])
        message = message[:100]
        if (message != recentMessage):
            showMessage(message)
            recentMessage = message
            logMessageToFile()
        else:
            showMessage(time.strftime(" %a, %b %d\n\n%m/%d/%Y"))
    except:
        pass

def scrollOldMessages():
    '''scroll through old messages'''
    global oldMessageShown
    if oldMessageShown == 0:
        recentMessage = ''
        checkForMessages()
    else:
        content = data.getRawDataFromFile('notifications.log');
        content = [x.strip() for x in content]
        content.reverse()
        showMessage(content[oldMessageShown])
    oldMessageShown = oldMessageShown + 1

# current messages
message = ''
currentMessage = ''
recentMessage = ''

# begin display an button listeners
subprocess.call(["/home/pi/RobbieAssistant/digole", "setRot90"])
subprocess.call(["/home/pi/RobbieAssistant/digole", "clear"])
subprocess.call(["/home/pi/RobbieAssistant/digole", "setColor", "255"])
refreshDisplay()
showMessage(time.strftime(" %a, %b %d\n\n%m/%d/%Y"))

# setup buttons and counts for timeout operations
oldMessageShown = 0
checkForMessageCount = 0
refreshDisplayCount = 0
redButton = Button(16)
blueButton = Button(26)

# start Robbie!
while True:
    redButton.when_pressed = clearDisplay
    blueButton.when_pressed = scrollOldMessages
    checkForMessageCount = checkForMessageCount + 1
    refreshDisplayCount = refreshDisplayCount + 1

    if refreshDisplayCount > 60000:
        refreshDisplay()
        refreshDisplayCount = 0

    if checkForMessageCount > 10000:
        checkForMessages()
        checkForMessageCount = 0

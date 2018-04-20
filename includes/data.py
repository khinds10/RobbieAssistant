#! /usr/bin/python
# Data helper functions to save and show human readable info
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, json, string, cgi, subprocess, os
import includes.settings as settings

def convertHumanReadable(seconds):
    """return days,hours,seconds for seconds in readable form"""
    return displayHumanReadableTime(seconds)

def convertToInt(integer):
    """convert to integer catch for NoneTypes"""
    try:
        return int(integer)
    except (Exception):
        return 0

def convertToString(value):
    """convert to string catch for NoneTypes"""
    try:
        return str(value)
    except (Exception):
        return ""

def displayHumanReadableTime(seconds, granularity=3):
    """display human readable units of time for given seconds"""
    intervals = (('d', 86400),('h', 3600),('m', 60),)
    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{}{}".format(value, name))
    return ''.join(result[:granularity])

def getJSONFromDataFile(fileName):
    """get JSON contents from file in question"""
    try:
        with open(settings.logFilesLocation + fileName) as myFile:    
            return json.load(myFile)
    except (Exception):
        return ""

def getRawDataFromFile(fileName):
    """get raw contents from file in question"""
    try:
        with open(settings.logFilesLocation + fileName) as myFile:
            return myFile.readlines()            
    except (Exception):
        return ""
        
def appendRawToFile(fileName, text):
    """append to data file raw text"""
    f = file(settings.logFilesLocation + fileName, "a")
    f.write(str(text))

def saveJSONObjToFile(fileName, JSONObj):
    """create or rewrite object to data file as JSON"""
    f = file(settings.logFilesLocation + fileName, "w")
    f.write(str(JSONObj.to_JSON()))
      
def checkFileExists(fileName):
    """check if data file by name exists or not"""
    return os.path.exists(settings.logFilesLocation + fileName)
          
def removeJSONFile(fileName):
    """delete JSON file in question"""
    try:
        os.remove(settings.logFilesLocation + fileName)
    except (Exception):
        pass

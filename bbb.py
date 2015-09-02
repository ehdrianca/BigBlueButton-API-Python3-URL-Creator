
"""
"
" bbb.py
"
" Python 3 BigBlueButton XML API and URL Creator
" Version: 0.1
"
" Copyright 2015 Success Office Systems, Regina, SK, Canada
" Author: Adrian Thompson
"
"""

"""
"
" Install:
" pip install xmltodict 
" Then copy this file to a location where your program can see it
"
"""

"""
"
" Use:
" from myApp.bbb import BigBlueButton
" BBB_Node1 = BigBlueButton("http://localhost", "12134") ### NO TRAILING SLASH ON URL
" createurl = BBB.create(
"     "name", "meetingID", "attendeePW", "moderatorPW", "addWelcome", "", "", "",
"     "", "", "", "", "", ""))
" resp = BBB.sendAndRecieve(createurl)
" joinMeetingURLString = BBB_Node1.join(
"     "Adrian Thompson", "meetingID", "attendeePW", resp['response']['createTime'],
"     "", "", "", "", "", ""
" )
"
" If your using Django you might, in a view, pull the data from a database and:
"     return HttpResponseRedirect(BBB_Node1.join(
"         request.GET['displayName'],
"         request.GET['meetingID'],
"         request.GET['password'],
"         resp['response']['createTime'],
"         "", "", "", "", "", "")
"     )
"
"""

import xmltodict
import hashlib
import urllib

class BigBlueButton(object):
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    "
    "  CLASS GLOBALS
    "
    """
    
    # Defined via Constructor
    API_URL = ""
    SHARED_SECRET = ""
    
    # Defined here
    LOGOUT_URL = "http://localhost/SConference/"
    WELCOME_MESSAGE = "Welcome to %%CONFNAME%%. Meeting info: Dial: %%DIALNUM%%, Conference: %%CONFNUM%%"
    
    # Constructor
    def __init__(self, apiUrl, sharedSecret):
        self.API_URL = apiUrl
        self.SHARED_SECRET = sharedSecret
    
    # Checksum
    def createChecksumQuery(self, queryString, call):
        strvar = "checksum="
        if(queryString != ""):
            strvar = "&checksum="
        return queryString + strvar + (hashlib.sha1(bytearray((call + queryString) + self.SHARED_SECRET, 'utf-8'))).hexdigest()
    
    # Converts XML server response to a dictionary
    def convertResponse(self, data):
        return xmltodict.parse(data)
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    "
    "  SERVER - Use asyc/threaded code instead as required
    "
    """
    
    def getServerResponse(self, url):
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            return str(response.read().decode("utf-8"))
        
    def sendAndRecieve(self, url):
        return self.convertResponse(self.getServerResponse(url))
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    "
    "  ADMIN
    "
    """

    def create(self, name, meetingID, attendeePW, moderatorPW, addWelcome,
               dialNumber, voiceBridge, webVoice, record, duration, meta,
               moderatorOnlyMessage, autoStartRecording,
               allowStartStopRecording):
        queryDict = {
            "name":name,
            "meetingID":meetingID,
            "attendeePW":attendeePW,
            "moderatorPW":moderatorPW,
            "welcome":self.WELCOME_MESSAGE + addWelcome,
            "addWelcome":addWelcome,
            "dialNumber":dialNumber,
            "voiceBridge":voiceBridge,
            "webVoice":webVoice,
            "logoutURL":self.LOGOUT_URL,
            "record":record,
            "duration":duration,
            "meta":meta,
            "moderatorOnlyMessage":moderatorOnlyMessage,
            "autoStartRecording":autoStartRecording,
            "allowStartStopRecording":allowStartStopRecording
        }
        queryString = urllib.parse.urlencode(queryDict)
        return self.API_URL + "/create?" + self.createChecksumQuery(queryString, "create")

    def join(self, fullName, meetingID, password, createTime, userID,
             webVoiceConf, configToken, avatarURL, redirect, clientURL):
        queryDict = {      
            "fullName":fullName,
            "meetingID":meetingID,
            "password":password,
            "createTime":createTime,
            "userID":userID,
            "webVoiceConf":webVoiceConf,
            "configToken":configToken,
            "avatarURL":avatarURL,
            "redirect":redirect,
            "clientURL":clientURL
        }
        queryString = urllib.parse.urlencode(queryDict)
        return self.API_URL + "/join?" + self.createChecksumQuery(queryString, "join")
    
    def end(self, meetingID, password):
        queryDict = {      
            "meetingID":meetingID,
            "password":password
        }
        queryString = urllib.parse.urlencode(queryDict)
        return self.API_URL + "/end?" + self.createChecksumQuery(queryString, "end")

    def getDefaultConfigXML(self):
        return self.API_URL + "/getDefaultConfigXML?" + self.createChecksumQuery("", "getDefaultConfigXML")

    def setConfigXML(self, meetingID, configXML):
        queryDict = {      
            "meetingID":meetingID,
            "configXML":configXML
        }
        queryString = urllib.parse.urlencode(queryDict)
        return self.API_URL + "/setConfigXML?" + self.createChecksumQuery(queryString, "setConfigXML")
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    "
    "  MONITORING
    "
    """
    
    def isMeetingRunning(self, meetingID):
        queryDict = {      
            "meetingID":meetingID
        }
        queryString = urllib.parse.urlencode(queryDict)
        return self.API_URL + "/isMeetingRunning?" + self.createChecksumQuery(queryString, "isMeetingRunning")

    def getMeetingInfo(self, meetingID, password):
        queryDict = {      
            "meetingID":meetingID,
            "password":password
        }
        queryString = urllib.parse.urlencode(queryDict)
        return self.API_URL + "/getMeetingInfo?" + self.createChecksumQuery(queryString, "getMeetingInfo")

    def getMeetings(self):
        return self.API_URL + "/getMeetings?" + self.createChecksumQuery("", "getMeetings")
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    "
    "  RECORDINGS
    "
    """
        
    def getRecordings(self, meetingID):
        queryDict = {      
            "meetingID":meetingID
        }
        queryString = urllib.parse.urlencode(queryDict)
        return self.API_URL + "/getRecordings?" + self.createChecksumQuery(queryString, "getRecordings")

    def publishRecordings(self, recordID, publish):
        queryDict = {      
            "recordID":recordID,
            "publish":publish
        }
        queryString = urllib.parse.urlencode(queryDict)
        return self.API_URL + "/publishRecordings?" + self.createChecksumQuery(queryString, "publishRecordings")

    def deleteRecordings(self, recordID):
        queryDict = {      
            "recordID":recordID
        }
        queryString = urllib.parse.urlencode(queryDict)
        return self.API_URL + "/deleteRecordings?" + self.createChecksumQuery(queryString, "deleteRecordings")



### FOR DEBUG ###
#python bbb.py
"""
if __name__ == '__main__':
    BBB = BigBlueButton("http://111.222.333.444/bigbluebutton/api", "sharedsecret")
    
    print("\ncreate\n")
    print(BBB.create("name", "meetingID", "attendeePW", "moderatorPW", "addWelcome", "", "", "",
                   "", "", "", "", "", ""))
    
    print("\njoin\n")
    print(BBB.join("Adrian Thompson", "meetingID", "attendeePW", "1441149421128", "", "", "", "", "", ""))
    
    print("\nend\n")
    print(BBB.end("meetingID", "password"))
    
    print("\ngetDefaultConfigXML\n")
    print(BBB.getDefaultConfigXML())
    
    print("\nsetConfigXML\n")
    print(BBB.setConfigXML("meetingID", "<xml>some xml stuff</xml>"))
    
    print("\nisMeetingRunning\n")
    print(BBB.isMeetingRunning("meetingID"))
    
    print("\ngetMeetingInfo\n")
    print(BBB.getMeetingInfo("meetingID", "password"))
    
    print("\ngetMeetings\n")
    print(BBB.getMeetings())
    
    print("\ngetRecordings\n")
    print(BBB.getRecordings("meetingID"))
    
    print("\npublishRecordings\n")
    print(BBB.publishRecordings("recordID", "publish"))
    
    print("\ndeleteRecordings\n")
    print(BBB.deleteRecordings("recordID"))
    
    print("\ngetServerResponse\n")
    print(BBB.getServerResponse('http://10.251.3.100/bigbluebutton/'))
    
    print("\nsendAndRecieve\n")
    print(BBB.sendAndRecieve(BBB.create("name", "meetingID", "attendeePW", "moderatorPW", "addWelcome", "", "", "", "", "", "", "", "", "")))
    
    print("\ncreateTime\n")
    resp = BBB.sendAndRecieve(BBB.create("name", "meetingID", "attendeePW", "moderatorPW", "addWelcome", "", "", "", "", "", "", "", "", ""))
    print(resp['response']['createTime'])
    
    print("\n")
"""

# BigBlueButton-API-Python3-URL-Creator
BigBlueButton Python 3 API URL Creator

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

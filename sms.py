#!/usr/bin/env python
 
import urllib2
import urllib
 
def sendSMS(uname, hashCode, numbers, sender, message, test):
    data =  urllib.urlencode({'username': uname, 'hash': hashCode, 'numbers': numbers,
        'message' : message, 'sender': sender, 'test' : test})
    data = data.encode('utf-8')
    request = urllib2.Request("http://api.textlocal.in/send/?")
    f = urllib2.urlopen(request, data)
    fr = f.read()
    return(fr)
 
# resp =  sendSMS('user', 'hash', '918123456789',
#     'Jims Autos', 'This is your message')
# print (resp)


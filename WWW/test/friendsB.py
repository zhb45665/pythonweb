#!/bin/python
# -*- coding:utf8 -*-
'''
Created on 2016年11月17日

@author: zhb
'''
import cgi
header = 'Content-Type:text/html \n'
formhtml = '''
<html>
    <head>
        <title>Friends CGI Demo</title>
    </head>
    <body>
        <h3>Friends list for:<i>new user</i></h3>
        <form action = '/cgi-bin/friendsB.py'>
            <b>Enter your name:</b>
            <input type = "hidden" name="action" value = "edit">
            <input type = "text" name ="person" value = "newuser" size=15>
            <p><b>how many friends do you have?</b>
            %s
            <p><input type="submit">
        </form>
    </body>
</html>
'''

fradio = '<input type = "radio" name = "howmany" value = "%s" %s> %s\n'
def showForm():
    friends = []
    for i in (0,10,25,50,100):
        checked = ''
        if i == 0:
            checked = 'checked'
        friends.append(fradio % (str(i),checked,str(i)))
    print('%s%s' % (header,formhtml % ''.join(friends)))
reshtml = '''
<html>
    <head>
        <title>Friends CGI Demo</title>
    </head>
    <body>
        <h3>Friends list for:<i>%s<i></h3>
        your name is :<b>%s</b><p>
        you have <b>%s </b>friends.
    </body>
</html>
'''    
def doResult(who,howmany):
    print((header+reshtml) % (who,who,howmany))

def process():
    form = cgi.FieldStorage()
    if 'person' in form:
        who = form['person'].value
    else:
        who = 'new user'
        
    if 'howmany' in form:
        howmany = form['howmany'].value
    else:
        howmany = 0
        
    if 'action' in form:
        doResult(who, howmany)
    else:
        showForm()
        
if __name__ == '__main__':
    process()
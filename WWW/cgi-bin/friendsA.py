#!/bin/python
# -*- coding:utf8 -*-
'''
Created on 2016��11��17��

@author: zhb
'''
import cgi
reshtml = ''' Content-type:text/html \r\n
<html>
    <head>
        <title>Friends CGI demo(dynamic screen)</title>
    </head>
    <body>
        <h3>Friends list for:<i>%s</i></h3>
        your name is :<b>%s</b><p>
        you have <b>%s </b>friends.
    </body>
</html>
'''
form = cgi.FieldStorage()
who = form['person'].value
howmany = form['howmany'].value
print(reshtml % (who,who,howmany))
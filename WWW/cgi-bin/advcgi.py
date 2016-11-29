#!/bin/python
# -*- coding:utf8 -*-
'''
Created on 2016年11月21日

@author: zhb
'''
from cgi import FieldStorage
from os import environ
from io import StringIO
from urllib.parse import quote,unquote
import string

class AdvCGI(object):
    header = 'Content-Type: text/html \r\n'
    url = '/cgi-bin/advcgi.py'
    formhtml = '''
    <html>
        <head>
            <title>Advance CGi Demo</title>
        </head>
        <body>
            <h2>Advance CGI Demo Form</h2>
            <form method = 'post' action = '%s' enctype = 'multipart/form-data'>
                <h3>my cookie seting</h3>
                <li>
                    <code>
                        <b>CPPuser = %s</b>
                    </code>
                </li>
                <h3>
                    enter cookie value<br>
                    <input name ='cookie' value='%s'>
                    (<i>optional</i>)
                </h3>
                <h3>
                    enter your name<br>
                    <input name = 'person' value = '%s'>
                    (<i>required</i>)
                </h3>
                <h3>what languages can you program in?
                (<i>at least one required</i>)</h3>
                %s
                <h3>
                    enter file to upload <small>（max size 4K）</small>
                </h3>
                <input type = 'file' name = 'upfile' value = '%s' size = 45>
                <p><input type = 'submit'>
            </form> 
        </body>
    </html>
    '''
    langSet = ('Python','Ruby','Java','C++','PHP','C','JaveScript')
    langItem = "<input type = 'checkbox' name = 'lang' value = '%s' %s> %s\n"
    def getCPPCookies(self):
        if 'HTTP_COOKIE' in environ:
            cookies = [x.strip() for x in environ['HTTP_COOKIE'].split(';')]
            for eachCookie in cookies:
                if (len(eachCookie) > 6 and eachCookie[:3] == 'CPP'):
                    tag = eachCookie[3:7]
                    try:
                        self.cookies[tag] = eval(unquote(eachCookie[8:]))
                    except:
                        self.cookies[tag] = unquote(eachCookie[8:])
            if 'info' not in self.cookies:
                self.cookies['info'] = ''
            if 'user' not in self.cookies:
                self.cookies['user'] = ''
        else:
            self.cookies['info'] = self.cookies['user'] = ''
        if self.cookies['info'] != '':
            self.who,langstr,self.fn = self.cookies['info'].split(':')
            self.langs = langstr.split(',')
        else:
            self.who = self.fn = ''
            self.langs = ['python']
    def showForm(self):
        self.getCPPCookies()
        
        langstr = []
        for eachlang in AdvCGI.langSet:
            langstr.append(AdvCGI.langItem % (eachlang,(' CHECKED' if eachlang in self.langs else ''),eachlang))
            if not ('user' in self.cookies and self.cookies['user']):
                cookStatus = '<i>(cookie has not been set yet)</i>'
                userCook = ''
            else:
                userCook = cookStatus = self.cookies['user']
        print('%s%s' % (AdvCGI.header,AdvCGI.formhtml % (AdvCGI.url,cookStatus,userCook,self.who,''.join(langstr),self.fn)))

    errhtml = '''
    <html>
        <head>
            <title>Advanced CGI Demo<title>
        <head>
        <body>
            <h3>ERROR</h3>
            <p><b>%s</b>
            <form>
                <input type = 'button' value = 'Back' onclick = 'window.hostory.back()'>
            </form>
        </body>
    </html>
    '''
    def showError(self):
        print((AdvCGI.header+AdvCGI.errhtml) % (self.error))
    reshtml = '''
    <html>
        <head>
            <title>Advanced CGI Demo</title>
        </head>
        <h2>your upload data</h2>
        <h3>your cookie value is:<b>%s</b></h3>
        <h3>your name is:<b>%s</b></h3>
        <h3>you can program in the following languages:</h3>
        <ul>%s<ul>
        <h3>
            your upload file ...<br>
            Name:<i>%s</i><br>
            Contents:
        </h3>
        <pre>%s<pre>
        Click <a href = '%s'><b>here</b></a> to return to form.
    </html>
    '''
    def setCPPCookies(self):
        for eachCookie in self.cookies.keys():
            print('Set-Cookie:CPP%s=%s;path/' % (eachCookie,quote(self.cookies[eachCookie])))
            
    def doResults(self):
        MAXBYTES = 4096*4096
        langlist = ''.join('<li>%s</><br>' % (eachlang for eachlang in self.langs))
        filedata = self.fp.read(MAXBYTES)
        if len(filedata) == MAXBYTES and f.read():
            filedata = '%s%s' % (filedata,'... <b><i>file truncated due to size</i></b>')
        self.fp.close()
        if filedata == '':
            filedata = '<b><i>(file not given or upload error)</i></b>'
        filename = self.fn
        if not ('user' in self.cookies and self.cookies['user']):
            cookStatus = '<i>(cookie  has not been set yet)</i>'
            userCook = ''
        else:
            userCook = cookStatus = self.cookies['user']
        self.cookies['info'] = ':'.join((self.who,','.join(self.langs),filename))
        self.setCPPCookies()
        print('%s%s' % (AdvCGI.header,AdvCGI.reshtml % (cookStatus,self.who,langlist,filename,filedata,AdvCGI.url)))
    
    def go(self):
        self.cookies = {}
        self.error = ''
        form = FieldStorage()
        if not form.keys():
            self.showForm()
            return
        if 'person' in form:
            self.who = form['person'].value.strip().title()
            if self.who == '':
                self.error = 'your name is required. (blank)'
        else:
            self.error = 'your name is required. (missing)'
        self.cookies['user'] = unquote(form['cookie'].value.strip()) if 'cookie' in form else ''
        if 'lang' in form:
            langdata = form['lang']
            if isinstance(langdata,list):
                self.langs = [eachlang.value for eachlang in langdata]
            else:
                self.langs = [langdata.value]
        else:
            self.error = 'at least one language required'
        if 'upfile' in form:
            upfile = form['upfile']
            self.fn = upfile.filename or ''
            if upfile.file:
                self.fp = upfile.file
            else:
                self.fp = StringIO('no data')
        else:
            self.fp = StringIO('no file')
            self.fn = ''
        if not self.error:
            self.doResults()
        else:
            self.showError()
if __name__ == '__main__':
    page = AdvCGI()
    page.go()
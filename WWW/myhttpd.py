#!/bin/python
# -*- coding:utf-8 -*-
'''
Created on 2016��11��16��

@author: zhb
'''

from http.server import BaseHTTPRequestHandler,HTTPServer
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            f = open(self.path[1:],'r')
            self.send_response(200)
            self.send_hander('Content-type','text/html')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        except IOError:
            self.send_error(400, 'File Not Found: %s' % self.path)
def main():
    try:
        server = HTTPServer(('',80),MyHandler)
        print('Welcome to the machine ...')
        print('Press ^C once or twice to quit.')
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received,shutting down server')
        server.socket.close()
if __name__ == '__main__':
    main()

# encoding: utf-8
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import pymysql
from conf import MYSQL_CONF
import random

HOST_NAME = 'localhost'
PORT_NUMBER = 5000


class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        paths = {
            '/get': {'status': 200}
        }

        if self.path in paths:
            self.respond(paths[self.path])
        else:
            self.respond({'status': 500})

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        conn = pymysql.connect(host=MYSQL_CONF['host'],
                               user=MYSQL_CONF['user'],
                               passwd=MYSQL_CONF['passwd'],
                               db=MYSQL_CONF['db'],
                               port=MYSQL_CONF['port'],
                               charset='utf8')
        cursor = conn.cursor()
        cursor.execute('select ip,port from proxypool')
        ip_list = []
        for row in cursor.fetchall():
            ip_list.append("%s:%s" % (row[0], row[1]))

        content = random.choice(ip_list)
        return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))


import time
import http.server
import json
from phv_eng import *

HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8080 # Maybe set this to 9000.

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        print (self.path)
        if self.path=='/new_ex':
            return self.new_exercise_header()
        return super().do_HEAD()
        
    def do_GET(self):
        print (self.path)
        if self.path=='/new_ex':
            return self.new_exercise()
        return super().do_GET()

    def new_exercise_header(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    def new_exercise(self):
        if not hasattr(self, "model"):
            self.model = Model()
            assert self.model.load("phv.lang"), "Model is not loaded"
            print ("Model is loaded")

        e, vars = self.model.randomExVars(4)
        json_string = self.model.jsonify(e, vars)
        print(json_string)

        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write(json_string.encode())

if __name__ == '__main__':
    server_class = http.server.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print (time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print (time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))

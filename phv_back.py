
import time
import http.server
import json
import os
import phv_eng
import json

HOST_NAME = ''
PORT_NUMBER = int(os.environ['PORT'])
NB_VARIANTS = 4

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        print (self.path)
        if self.path=='/new_ex':
            return self.json_header()
        return super().do_HEAD()
        
    def do_GET(self):
        print (self.path)
        if self.path=='/new_ex':
            return self.new_exercise()
        if self.path.startswith('/def='):
            return self.get_definition(self.path[5:])
        return super().do_GET()

    def check_model(self):
        if not hasattr(self, "model"):
            self.model = phv_eng.Model()
            assert self.model.load("phv2.lang"), "Model is not loaded"
            print ("Model is loaded")
    
    def json_header(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    def send(self, json_string):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write(json_string.encode())

    def new_exercise(self):
        self.check_model()
        e, vars = self.model.randomExVars(NB_VARIANTS)
        json_string = self.model.jsonify(e, vars)
        #print(json_string)
        self.send(json_string)

    def get_definition(self, verb):
        self.check_model()
        verb2 = verb.replace("%20", " ")
        print (verb2)
        d = self.model.getDefinition(verb2)
        print (d)
        dl = d.split("\n")        
        data = {}
        data["definition"] = dl
        json_string = json.dumps(data)
        self.send(json_string)
        

if __name__ == '__main__':
    """
    m = phv_eng.Model()
    assert m.load("phv2.lang"), "Model is not loaded"
    print ("Model is loaded")
    print (m.getDefinition("give out"))
    """
    
    server_class = http.server.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print (time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print (time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))

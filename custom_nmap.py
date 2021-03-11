import requests

class DirScanner():
    def __init__(self, ip):
        self.ip   = ip

    def scan(self, web_path):
        r       = requests.get(self.ip)
        status  = r.status_code
        # if the server comes back with a 200 code 
        # then it will save the web path.
        if int(status) == 200:
             print("UP")


d = DirScanner("https://utica.edu")
d.scan()
import requests
import threading

class DirScanner():
    def __init__(self, ip):
        self.ip   = ip

    def scan(self, web_path):
        # ASSUMES that the IP that was given
        # already has a / at the end of the URL
        # Will add that function after I get it working
        try:
            r       = requests.get(self.ip + web_path)
            status  = r.status_code
            # if the server comes back with a 200 code 
            # then it will save the web path.
            # we used the int method to convert the 
            # status into an integer
            print(status)
            if int(status) == 200:
                 print("UP")
        except as e:
            print(e)


    def run(self):
        file = open("lists/dirsearch.txt", 'r')
        line = file.readlines()
        for l in line:
            self.scan(l)
            t1 = threading.Thread(target =self.scan(l))
            t1.start()



d = DirScanner("https://utica.edu/")
d.run()
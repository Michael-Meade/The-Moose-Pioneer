import requests
# import the utils class
import u
import optparse
import threading
# this class can be used to save the results from
# the scan in a txt file. Later after the scan
# it will read the dir_scan.txt file and create 
# a HTML File. The plan is to 
class DirScanReports():
    def __init__(self, ip, web_path):
        self.ip       = ip
        self.web_path = web_path

    def write_file(self):
        write = u.FileUtils(self.ip)
        write.write_text("dir_scan.txt", str(self.web_path) + "\n")


# this is the class that does the Scanning.
# The scan method uses multi thread to make 
# the scan faster. If the status code is 200
# the code will save the file path to the file
# using the reports class.
# the code will rescue any errors that are 
# because of to many redirects.  
# NOTE: it might be possible to increase the
# amount of redirects  
# 
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
            print(self.ip + web_path)
            # if the server comes back with a 200 code 
            # then it will save the web path.
            # we used the int method to convert the 
            # status into an integer
            if int(status) == 200:
                # removes https & http from ip so we we can create a file
                new_ip = self.ip.replace("https://", "").replace("http://", "").replace("/", "")
                # add the new_ip & web path together to make a varaible 
                # named url
                url = str(new_ip) + "/" + str(web_path)
                DirScanReports(new_ip, str(url)).write_file()

        except requests.exceptions.TooManyRedirects as f:
            print(f)

    # This needs to be called
    def run(self):
        # reads from the dir list.
        # In the future it would
        # be cool to add more lists
        file = open("lists/dirsearch.txt", 'r')
        line = file.readlines()
        for l in line:
            # thread it
            t1 = threading.Thread(target =self.scan(l))
            t1.start()


def main():
    parser = optparse.OptionParser("usage: python3 dir_scanner.py -H <host>")
    parser.add_option("-H", dest='ip', type="string", help="IP")
    (options, args) = parser.parse_args()
    # creates strings with the values of the input
    ip   = options.ip
    # checks to make sure they are not empty
    if (ip == None):
        print(parser.usage)
        exit(0)
    else:
        # this gets the last char of the
        # ip variable and if it is not a "/"
        # then it will add one to the ip. 
        if ip[-1] != "/":
            ip = ip + "/"



        d = DirScanner(ip)
        d.run()



if __name__ == '__main__':
    main()
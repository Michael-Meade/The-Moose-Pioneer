import os
import shutil
import json
import csv
import sys
import shutil
# imports the utils class
import u
from datetime import date
import time
class Subdomain:
    def __init__(self, domain):
        self.domain  = domain

    def command(self):
        # replaces "targetdomain" w/ the domain inputed.
        return "cd subdomain3 & python brutedns.py -d targetdomain -s high -l 5".replace("targetdomain", self.domain)

    def move_results(self):
        source = os.path.join("subdomain3", "result", self.domain)
        file_names = os.listdir(source)
        try:
            for file_name in file_names:
                if not os.path.exists(os.path.join("scans", self.domain, file_name)):
                    # rename the files so we can get the current
                    #os.rename(os.path.join("subdomain3", "result", self.domain, file_name), os.path.join("subdomain3", "result", self.domain, str(time.time())  + file_name ))
                    shutil.move(os.path.join("subdomain3", "result", self.domain, file_name), os.path.join("scans", self.domain))


            shutil.move(os.path.join("subdomain3", "result", self.domain, file_name), os.path.join("scans", self.domain))
        except:
            # Maybe at a later time work on this.
            print("ERROR WITHE COPYING FILE: " + file_name) 

    def convert_json(self):
        # stores the FileUtils class as a variable
        write = u.FileUtils(self.domain)

        write.create_directory(os.path.join("scans", str(self.domain)))
        # converts the csv file into JSON. first reads csv and then converts to JSON.
        file  = open("scans/" + self.domain  + "/" + self.domain + ".csv", "r")
        d     = csv.DictReader(file)
        csv_r = list(d)
        
        t = u.Template()
        # this calls gets the Read() class
        # we store it as a instance variable 
        # so we can get the first half of the HMTL and
        # the last part of the HTML. 
        r = u.Read()
        html_out = []
        #html_out.append(r.html_start())
        html_out.append("<br><br>")
        msg = "<center><font color=white>Subdomains</font></center>"
        html_out.append(msg)
        html_out.append(r.html_table_subdomain_start())
        for i in csv_r:
            ip     = i["IP"]
            domain = i["DOMAIN"]
            cdn    = i["CDN"]
            cname  = i["CNAME"]
            ps = t.subdomain(str(ip), domain, cdn, cname)
            html_out.append(ps)

        html_out.append(r.html_table_end())
        msg = "<center><font color=white>The table above is the results from the Subdomain3 scan.</font></center>"
        html_out.append(msg)
        html_out.append(r.html_end())
        html = '\n'.join(html_out)
        write.write_text("ports_scan.html", str(html))

    def run(self):
        cmd = self.command()
        os.system(cmd)
        self.move_results()
        self.convert_json()



#s = Subdomain("utica.edu")
#s.move_results()
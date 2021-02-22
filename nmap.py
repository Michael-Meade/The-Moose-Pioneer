import nmap3
import json
import os
class Read():
    def html_start(self):
        r = open("templates/port_scan_template_start.html",'r')
        return r.read()

    def html_end(self):
        r = open("templates/port_scan_template_end.html",'r')
        return r.read()


class Template():
    def port_scan(self, name, protocol, portid, state, reason):
        return "<tr><td>" + name + "</td>\n" + "<td>" + protocol + "</td>\n" + '<td>' + portid + "</td>\n" + "<td>" + state + "</td>\n" + "<td>" + reason + "</td></tr>" 




class FileUtils:
    def __init__(self, ip):
        self.ip = ip
        # creaets an scan directory if 
        # it does not exist. This is 
        # where all the other stuff is stored.
        # When the FileUtils class is called it will 
        # create directories. 
        self.create_directory("scans")
        # creates a directry for the IP
        self.create_directory(os.path.join("scans", ip))


    def create_directory(self, name):
        if not os.path.exists(name):
            os.makedirs(name)

    # Makes it easy to save the output to a text file
    def write_text(self, file_name, data):
        with open(os.path.join("scans", self.ip, file_name), 'w') as outfile:
            outfile.write(data)

    # Makes it easy to save the output to a json file. 
    def write_json(self,ip,  file_name, data):
        with open(os.path.join("scans", ip, file_name), 'w') as outfile:
            json.dump(data, outfile)


class Scan():
    def __init__(self, ip):
        self.ip   = ip
        # creates an one instance of 
        # nmap so we all we have to do is
        # do:  self.nmap.nmap_version_detection(self.ip)aaaaa
        # For python to use the variable. WE NEED to have self. infront
        self.nmap = nmap3.Nmap()


    def service_version(self):
        # get services versions
        result = self.nmap.nmap_version_detection(self.ip)
        print(result)

    def top_port_scan(self):
        # Scan the top ports
        result = self.nmap.scan_top_ports(self.ip)
        # nmap outputs the results in JSON 
        # The key of the JSON is the IP 
        # the of the target. This is where 
        # we get the IP. This is stored as the 
        # variable IP so we can use later.
        ip   = list(result.keys())[0]
        scan = list(result[ip]["ports"])
        write = FileUtils(ip)
        t = Template()
        # this calls gets the Read() class
        # we store it as a instance variable 
        # so we can get the first half of the HMTL and
        # the last part of the HTML. 
        r = Read()
        html_out = []
        # adds the first part of the HTML file to
        # the list. like the CSS part, the html and body 
        html_out.append(r.html_start())
        for i in scan:
            name      = i['service']['name']
            protocol  = i['protocol']
            portid    = i['portid']
            state     = i['state']
            reason    = i['reason']
            # Takes the input ( name, protocolm etc) and adds HTML to to make the 
            # rows of the tables
            ps = t.port_scan(name, protocol, portid, state, reason)
            # earlier in the code we called the html_start method
            # and storedi to in a list. We now add the rows of the HMTL table to 
            # the list
            html_out.append(ps)
        

        msg = "<center>The table below shows the results of the port scan on (IP).<br></center>"
        html_out.append(str(msg.replace("(IP)", ip)))
        # adds the closing stuff so the  browser will show it the right way.
        html_out.append(r.html_end())
        html = '\n'.join(html_out)
        write.write_text("ports_scan.html", str(html))

scan = Scan("hackex.net")
scan.top_port_scan()
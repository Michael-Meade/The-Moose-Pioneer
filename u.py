import os
import json
import sys
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
        print(self.ip)
        self.create_directory(os.path.join("scans", ip))


    def create_directory(self, name):
        if not os.path.exists(name):
            os.makedirs(name)

    # Makes it easy to save the output to a text file
    def write_text(self, file_name, data):
        with open(os.path.join("scans", self.ip, file_name), 'a') as outfile:
            outfile.write(data)

    # Makes it easy to save the output to a json file. 
    def write_json(self,ip,  file_name, data):
        with open(os.path.join("scans", ip, file_name), 'w') as outfile:
            json.dump(data, outfile)


class Read:
    def html_start(self):
        # used to start the HTML file
        r = open("templates/html_template_start.html",'r')
        return r.read()

    def html_end(self):
        # used to closed the HTML file
        r = open("templates/html_template_end.html",'r')
        return r.read()

    def html_table_end(self):
        # used to end the HTML file
        r = open("templates/html_table_template_end.html",'r')
        return r.read()

    def html_table_start(self):
        # used to start the HTML file
        r = open("templates/html_table_template_start.html",'r')
        return r.read()

    def html_service_start(self):
        # used for service scan
        r = open("templates/html_table_service.html",'r')
        return r.read()

    def html_table_dns_start(self):
        r = open("templates/html_table_template_start_dns.html", "r")
        return r.read()

    def html_table_subdomain_start(self):
        r = open("templates/html_subdomain_template_start.html")
        return r.read()

class Template:
    # the template class job is to create the rows of the HTML table
    # The \n & \t needs to be there. This gives the HTML table 
    # a pretty format. This makes it easier to edit the HTML report later.
    def port_scan(self, name, protocol, portid, state, reason):
        return "\t<tr>\n\t\t<td>" + name + "</td>\n" + "\t\t<td>" + protocol + "</td>\n" + '\t\t<td>' + portid + "</td>\n" + "\t\t<td>" + state + "</td>\n" + "\t\t<td>" + reason + "</td>\n\t</tr>\n" 

    def service_scan(self, name, product, version, extrainfo, portid, state):
        return "\t<tr>\n\t\t<td>" + name + "</td>\n" + "\t\t<td>" + product + "</td>\n" + "\t\t<td>" + version + "</td>\n" + "\t\t<td>" + extrainfo + "</td>\n" + "\t\t<td>" + portid + "</td>\n" + "\t\t<td>" + state + "</td>\n\t</tr>\n"

    def subdomain(self, ip, domain, cdn, cname):
        return "\t<tr>\n\t\t<td>" + ip + "</td>\n" + "\t\t<td>" + domain + "</td>\n" + "\t\t<td>" + cdn + "</td>\n" + "\t\t<td>" + cname + "</td>\n\t</tr>\n"
    
    def dns_scan(self, address, hostname):
        return "\t<tr>\n\t\t<td>" + address + "</td>\n" + "\t\t<td>" + hostname + "</td>\n\t</tr>\n"
import nmap3
import json
import os
class Read():
    def html_start(self):
        r = open("templates/html_template_start.html",'r')
        return r.read()

    def html_end(self):
        r = open("templates/html_template_end.html",'r')
        return r.read()

    def html_table_end(self):
        r = open("templates/html_table_template_end.html",'r')
        return r.read()

    def html_table_start(self):
        r = open("templates/html_table_template_start.html",'r')
        return r.read()
    def html_table_start(self):
        r = open("templates/html_table_template_start.html",'r')
        return r.read()
    def html_service_start(self):
        r = open("templates/html_table_service.html",'r')
        return r.read()

class Template():
    def port_scan(self, name, protocol, portid, state, reason):
        return "<tr><td>" + name + "</td>\n" + "<td>" + protocol + "</td>\n" + '<td>' + portid + "</td>\n" + "<td>" + state + "</td>\n" + "<td>" + reason + "</td></tr>" 

    def service_scan(self, name, product, version, extrainfo, portid, state):
        return "<tr><td style='white'>" + name + "</td>\n" + "<td style='white'>" + product + "</td>\n" + "<td style='white'>" + version + "</td>\n" + "<td>" + extrainfo + "</td>\n" + "<td>" + portid + "</td>\n" + "<td>" + state + "</td></tr>"


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
        with open(os.path.join("scans", self.ip, file_name), 'a') as outfile:
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
        #html_out.append(r.html_start())
        html_out.append("<br><br>")
        html_out.append(r.html_service_start())
        for i in scan:
            #print(i['service']['product'])
            name      = i['service']['name']
            portid    = i['portid']
            state     = i['state']
            if 'product' in i['service']:
                #print(i["service"]["product"])
                product   = i['service']['product']
            else:
                product   = "Null"


            if 'extrainfo' in i['service']:
                extrainfo = i['service']['extrainfo']
            else:
                extrainfo = "Null"


            if 'version' in i['service']:
                version  = i['service']['version']
            else:
                version  = "Null"

            
           
            
            ps = t.service_scan(name, product, version, extrainfo, portid, state)
            html_out.append(ps)
        
        html_out.append(r.html_table_end())
        msg = "<center>The table above shows more information about the services that are running on (IP).</center>"
        html_out.append(msg.replace("(IP)", ip))
        html_out.append(r.html_end())
        html = '\n'.join(html_out)
        write.write_text("ports_scan.html", str(html))

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
        html_out.append(r.html_table_start())
        open_port = []
        for i in scan:
            name      = i['service']['name']
            protocol  = i['protocol']
            portid    = i['portid']
            state     = i['state']
            reason    = i['reason']
            if str(state) == "open":
                open_port.append([ str(state), str(name), str(portid)])


            # Takes the input ( name, protocolm etc) and adds HTML to to make the 
            # rows of the tables
            ps = t.port_scan(name, protocol, portid, state, reason)
            # earlier in the code we called the html_start method
            # and storedi to in a list. We now add the rows of the HMTL table to 
            # the list

            html_out.append(ps)


        msg  = "<center>The table below shows the results of the port scan on (IP).<br></center>"
        html_out.append(str(msg.replace("(IP)", ip)))
        # adds the closing stuff so the  browser will show it the right way.
        html_out.append(r.html_table_end())
        if len(open_port) > 0:
            msg3 = "The (SERVICE) service has port (PORT) open."
            msg_list = []
            msg_list.append("<center><br>")
            for i in open_port:

                msg_list.append(str(msg3.replace("(SERVICE)", i[1]).replace("(PORT)", i[2])))


        msg_port = ' '.join(msg_list)
        html = '\n'.join(html_out)
        html_out.append(msg_port)
        html_out.append("</center>")
        html = '\n'.join(html_out)
        #html_out.append(r.html_end())
        html = '\n'.join(html_out)
        msg_list.append("<br><br>")
        write.write_text("ports_scan.html", str(html))

scan = Scan("utica.edu")
scan.top_port_scan()
scan.service_version()
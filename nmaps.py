import nmap3
import json
import sys
# imports the utils class ( u.py )
import u
# imports the subdomain class ( sub.py )
import sub
import os
class Scan:
    def __init__(self, ip):
        self.ip   = ip
        # creates an one instance of 
        # nmap so we all we have to do is
        # do:  self.nmap.nmap_version_detection(self.ip)
        # For python to use the variable. WE NEED to have self. infront
        self.nmap = nmap3.Nmap()

    def service_version(self):
        # used to save the file
        # this is different then ip because
        # the variable ip gets its result from 
        # the scan results.
        ips = self.ip
        # get services versions
        result = self.nmap.nmap_version_detection(self.ip)
        ip   = list(result.keys())[0]
        scan = list(result[ip]["ports"])
        write = u.FileUtils(ips)
        t = u.Template()
        # this calls gets the Read() class
        # we store it as a instance variable 
        # so we can get the first half of the HMTL and
        # the last part of the HTML. 
        r = u.Read()
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
        msg = "<center><font color=white>The table above shows more information about the services that are running on (IP).</font></center>"
        # replaces (IP) with the address of the host being scanned.
        html_out.append(msg.replace("(IP)", ip))
        html_out.append(r.html_end())
        html = '\n'.join(html_out)
        write.write_text("ports_scan.html", str(html))

    def dns_scan(self):
        results = self.nmap.nmap_dns_brute_script(self.ip)
        ip      = self.ip
        write   = u.FileUtils(ip)
        t = u.Template()
        # this calls gets the Read() class
        # we store it as a instance variable 
        # so we can get the first half of the HMTL and
        # the last part of the HTML. 
        r = u.Read()
        html_out = []
        html_out.append("<br><br>")
        html_out.append(r.html_table_dns_start())
        for i in results:
            addr     = i['address']
            hostname = i['hostname']
            dns = t.dns_scan(addr, hostname)
            html_out.append(dns)

        msg  = "<center><font  color=white>The table below shows the results of the DNS scan of (IP).<br></font></center>"
        # replaces '(IP)' with the Ip of the host
        html_out.append(str(msg.replace("(IP)", ip)))
        html_out.append(r.html_table_end())
        html_out.append(r.html_end())
        html = '\n'.join(html_out)
        write.write_text("ports_scan.html", str(html))

    def top_port_scan(self):
        # this is for the file
        ips = self.ip
        # Scan the top ports
        result = self.nmap.scan_top_ports(self.ip)
        # nmap outputs the results in JSON 
        # The key of the JSON is the IP 
        # the of the target. This is where 
        # we get the IP. This is stored as the 
        # variable IP so we can use later.
        ip   = list(result.keys())[0]
        scan = list(result[ip]["ports"])
        write = u.FileUtils(ips)
        t = u.Template()
        # this calls gets the Read() class
        # we store it as a instance variable 
        # so we can get the first half of the HMTL and
        # the last part of the HTML. 
        r = u.Read()
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

        msg  = "<center><font color=white>The table below shows the results of the port scan on (IP).<br></font></center>"
        html_out.append(str(msg.replace("(IP)", ip)))
        # adds the closing stuff so the  browser will show it the right way.
        html_out.append(r.html_table_end())
        if len(open_port) > 0:
            msg3 = "<font color=white>The (SERVICE) service has port (PORT) open.</font>"
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




def basic_scan(domain):
    # basic scan currently is able to:
        # - Top port scan
        # - Service scan
        # - DNS scan
        # - Subdomain3
    scan = Scan(domain)
    scan.top_port_scan()
    scan.service_version()
    scan.dns_scan()
    s = sub.Subdomain(domain)
    s.run()    




basic_scan("hulu.com")
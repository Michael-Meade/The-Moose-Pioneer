# The-Moose-Pioneer



### scans folder

The scan folder is where all the results of the scan go for that domain. Inside the scans directory the code will create a new folder of the domain or IP that was inputed. For example, if we scan the IP 127.0.0.1 the code will create a new directory inside the scans folder with the name of 127.0.0.1. Inside 127.0.0.1 is where the program will store all the results.


### Template class
The template class is where we create the HTML table rows. The script will parse the JSON file of the results scan and create a HTML row. The script will append each row of the HTML table into a list. At the very end we join each element of the list and create the table. Each method in this class is used for a certain task. Currently, as of 2/24/2021 the script is able to create HTML tables for:
port_scan, service_scan, dns_scan. 


### FileUtils class
This class is used for creating the output. It currently supports, JSON and text. But it could output a file in any extension because you could name the file any name and it is assumed that when the programmer uses the method that they also include an file extension. 


### Subdomain3

It is assumed that subdomain3 is already installed. You might need to remove the subdomain3 directory and download the current version.  Support to have it auto install will most likely be added at a later time
You could use the following command or go to <a href="https://github.com/yanxiu0614/subdomain3">subdomain3</a>

```
git clone https://github.com/yanxiu0614/subdomain3.git
```

This project assumes that the subdomain3 directory is in the projects main directory. This is important becuase the subdomain.py file will use Python's ```os``` module to cd into the subdomain3 directory. The subdomain class currently has one command but others can be added later. By default the class will use & run the following command:

```
cd subdomain3 & python brutedns.py -d targetdomain -s high -l 5
```
The class will use Python's replace method to replace ```targetdomain``` with the domain or IP that was inputed.  The run method will call the command method in which will return the command above, the code will then use Python's ```os``` module to run the command. 

The code for subdomain will always output the results of the scan in the follow directory path:

```subdomain3/results/domain```
Two ```csv``` files should be inside that directory after the scan, the subdomain class will then move the contents of that directory and move the files into the scan folder. 
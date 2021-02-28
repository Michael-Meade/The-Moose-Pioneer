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
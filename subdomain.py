import os
import shutil
class Subdomain:
    def __init__(self, domain):
        self.domain  = domain

    def command(self):
        # replaces "targetdomain" w/ the domain inputed.
        return "cd subdomain3 & python brutedns.py -d targetdomain -s high -l 5".replace("targetdomain", self.domain)

    def move_results(self):
        shutil.move('subdomain3/result/' + self.domain + "/", 'scans/' + self.domain + "/")
    

    def run(self):
        cmd = self.command()
        os.system(cmd)
        self.move_results()

b = Subdomain("hackex.net")

b.run()
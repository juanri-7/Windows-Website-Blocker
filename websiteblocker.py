import time
from datetime import datetime as dt
import os
import threading

class website_blocker:
    
    # hostpath must have double \\ format to prevent string complications ?
    # C:\Windows\System32\drivers\etc
    def __init__(self, hostpath="C:\\Windows\\System32\\drivers\\etc", hostid="127.0.0.1"):
        self.hostpath = hostpath
        self.hostid = hostid
        self.thread1 = None
        self.stop_thread = threading.Event()

    # create sites.txt file if DNE
    # adds websites in "hostid"+" "+"website"+"\n" format
    # where sites is a list of string sites, sites = ["www.website.com"]
    def add_sites(self, sites):
        if isinstance(sites, list) == True:
            with open("sites.txt", "w+") as sitefile:
                content = sitefile.read()
                for website in sites:
                    if website in content:
                        pass
                    else:
                        sitefile.write(self.hostid + " " + website + "\n")
            return
        else:
            print("The sites must be in list format.")
            return

    # check if sites.txt exists first
    # if it does, delete the file, else return message
    def remove_all_sites(self):
        if os.path.exists("sites.txt"):
            os.remove("sites.txt")
            return
        else:
            print("There are no sites currently stored to block.")
            return
    
    # check if sites.txt exists first
    # if it does, read through and starting at beginning,
    # rewrite everyline except for one you want to remove
    def remove_one_site(self, site):
        if os.path.exists("sites.txt"):
            with open("sites.txt", "r+") as sitefile:
                content = sitefile.readlines()
            os.remove("sites.txt")
            with open("sites.txt", "w") as newsitefile:
                for line in content:
                    if site not in line:
                        newsitefile.write(line)
                    else:
                        pass
            return
        else:
            print("There are no sites currently stored to block.")
            return

    # reads out sites in existing file
    def show_sites(self):
        if os.path.exists("sites.txt"):
            with open("sites.txt", "r") as sitefile:
                for line in sitefile:
                    print(line)
            return
        else:
            print("There are no sites currently stored to block.")
            return

    # resets host file to original, removing previously added site restrictions
    # prevents us from adding redundant sites
    # also resets timer
    def reset_host(self):
        with open("originalhost.txt", "r") as originalhostfile:
            with open(self.hostpath + "\\hosts", "w") as hostfile:
                hostfile.write("\n")
                for line in originalhostfile:
                    hostfile.write(line)
        return
    
    # calls reset_host first
    # add contents of sites.txt to end of host file
    def add_sites_host(self):
        #self.reset_host()
        with open("sites.txt","r") as sitefile:
            with open(self.hostpath + "\\hosts", "a") as hostfile:
                hostfile.write("\n")
                for line in sitefile:
                    hostfile.write(line)
        return

    # calculates how much time is left before sites are unblocked
    def duration_left(self):
        pass

    # executes actual blocking features
    # starthour/endhour must be using time format user's computer is using
    # handle functionality for 24 and non-24 hour formats
    def block_execute(self, starthour, endhour, startminute=0, endminute=0):
        self.reset_host()
        while not self.stop_thread.is_set():
            if dt.now() < dt(dt.now().year, dt.now().month, dt.now().day, starthour, startminute):
                continue
            else:
                break

        if dt(dt.now().year, dt.now().month, dt.now().day, starthour, startminute) < dt.now() < dt(dt.now().year, dt.now().month, dt.now().day, endhour, endminute):
            self.add_sites_host()
        while not self.stop_thread.is_set():
            if dt.now() < dt(dt.now().year, dt.now().month, dt.now().day, endhour, endminute):
                continue
            else:
                break
        self.reset_host()
        return
    

if __name__ == "__main__":
    a = website_blocker("C:\\Windows\\System32\\drivers\\etc", "127.0.0.1" )
    #a.reset_host()
    sites = ["youtube.com","www.youtube.com"]
    sites2 = "www.google.com"
    #a.add_sites(sites)
    a.remove_all_sites()
    #a.remove_one_site(sites2)
    #a.show_sites()
    #a.add_sites_host()
    a.reset_host()
    #a.block_execute(15,15,0,29)
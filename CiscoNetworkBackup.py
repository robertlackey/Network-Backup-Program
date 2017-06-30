import time
import os
import paramiko
import datetime
from paramiko import client
from os import path
from datetime import datetime
from time import strftime, sleep
###############################
day_of_year = datetime.now().timetuple().tm_yday
now = datetime.now ()
abbrev_month = datetime.now()
abbrev_yr = datetime.now()
current_day = now.day
current_year = now.year
CONFIGSTR = "Device Configs on "
JULIANDATESTR = abbrev_yr.strftime('%y') + str(day_of_year) + " "
TIMESTAMP = '%s %s %s' % (abbrev_month.strftime('%b'), now.day, now.year)
FULLNAME = CONFIGSTR + JULIANDATESTR + TIMESTAMP
###############################
#storing the path in a variable
#THIS IS FOR LINUX PC/SERVER AND WILL NEED TO BE MODIFIED IF USED ON WINDOWS OS
CONFIGDIR = str(FULLNAME)
###############################
TESTDEV0 = "TESTDEV0.txt"
TESTDEV1 = "TESTDEV1.txt"
###############################
TESTDEV0DIR = os.path.join(CONFIGDIR, TESTDEV0)
TESTDEV1DIR = os.path.join(CONFIGDIR, TESTDEV1)
###############################
username = "***ENTER USERNAME HERE***"
password = '***ENTER PASSWORD HERE***'
###############################
hosts = [
##*** CISCO DEVICE IPs ***##
        #TESTDEV0 IP
        '***ENTER 1ST IP HERE***',
        #TESTDEV1 IP
        '***ENTER 2ND IP HERE***',
        ]
###############################
#***ADD, CHANGE, OR REMOVE ANY COMMANDS THAT ARE NECESSARY FOR YOU***
commands = [
        'en' + '\n',
        password + '\n',
        'terminal pager 0' + '\n' + '\n',
        'sh clock' + '\n' + '\n' + '\n' + '\n',
        'sh ver' + '\n' + '\n' + '\n' + '\n' + '\n',
        'sh run access-group' + '\n' + '\n'+ '\n' + '\n' + '\n',
        'sh run' + '\n', 'exit' + '\n'
        ]
###############################
class ssh:
    client = None
###############################
    def create_folder():
        #Change to newpath
        if os.path.exists(testpath):
            print "Path Exists Already"
        elif not os.path.exists(testpath):
            os.makedirs(testpath)
            print "creating folder @ " + testpath
###############################
    def __init__(self, address, username, password):
            # Let the user know we're connecting to the device
            print "Connecting to device."
            # Create a new SSH client
            self.client = paramiko.SSHClient()
            # The following line is required if you want the script to be able to access a server that's not yet in the known_hosts file
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # Make the connection
            self.client.connect(address, username=username, password=password, look_for_keys=False)
            print "Connected"
###############################
    def sendCommand(self, command):
        time.sleep(20)
        chan = self.client.invoke_shell()
        print "sending commands"
        for command in commands:
            chan.send(command)
        clientbuffer = []
        while not chan.exit_status_ready():
            if chan.recv_ready():
                clientbuffer.append(chan.recv(9999))
        self.clientoutput = ''.join(clientbuffer)
        self.client.close()
        print self.clientoutput
###############################
    def TESTDEV0_File(self):
        if (path.isfile(TESTDEV0DIR)):
            print "File already exists @" + str(TESTDEV0DIR)
        elif not(path.isfile(TESTDEV0DIR)):
            f = open(os.path.join(testpath, TESTDEV0), 'w')
            with open(os.path.join(testpath, TESTDEV0), 'w') as f:
                f.write('\n' + self.clientoutput)
                f.close
    def TESTDEV1_File(self):
        if (path.isfile(TESTDEV1DIR)):
            print "File already exists @" + str(TESTDEV1DIR)
        elif not(path.isfile(TESTDEV1DIR)):
            f = open(os.path.join(testpath, TESTDEV1), 'w')
            with open(os.path.join(testpath, TESTDEV1), 'w') as f:
                f.write('\n' + self.clientoutput)
                f.close
    create_folder()

if __name__ == '__main__':
    TD0 = ssh(hosts[0], username, password)
    TD0.sendCommand(commands)
    TD0.TESTDEV0_File()

    TD1 = ssh(hosts[1], username, password)
    TD1.sendCommand(commands)
    TD1.TESTDEV1_File()

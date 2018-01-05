#-------------------------------------------------------------------------------
# Python Script to Automate Device Backups
import time
import os
import paramiko
import datetime
import pwd
import grp
from paramiko import client
from os import path
from datetime import datetime
from time import strftime, sleep
##################################
#julian date string format = yeardayofyear ex.173
day_of_year = datetime.now().timetuple().tm_yday
now = datetime.now ()
#Adds 0's in front of julian date.
#format = yeardayofyear ex. 17003
jdstr = now.strftime('%j')
#calls the 2-digit month
abbrev_month = datetime.now()
#calls the 2-digit year
abbrev_yr = datetime.now()
#calls the 2-digit day
abbrev_day = datetime.now()
CONFIGSTR = "Configs on "
JULIANDATESTR = abbrev_yr.strftime('%y') + str(jdstr) + " "
TIMESTAMP = '%s %s %s' % (abbrev_month.strftime('%b'), abbrev_day.strftime('%d'), now.year)
FULLNAME = CONFIGSTR + JULIANDATESTR + TIMESTAMP
###############################
##stores the path in a variable and adds the naming variable above
###############################
CONFIGPATH = os.path.abspath("/home/")
os.chdir(CONFIGPATH)
CONFIGDIR = str(FULLNAME)
###############################
##creates the specific file names to be used in the
##create_file functions later
###############################
TESTDEV0 = "TESTDEV0.txt"
TESTDEV1 = "TESTDEV1.txt"
###############################
##This joins the path to the directory
##This will be used in the create_file function later
###############################
TESTDEV0DIR = os.path.join(CONFIGDIR, TESTDEV0)
TESTDEV1DIR = os.path.join(CONFIGDIR, TESTDEV1)
###############################
username = "ENTER USERNAME HERE"
password = "ENTER PASSWORD HERE"
##################################
##Host IPs for accessing the devices
##################################
hosts = [
##*** Devices ***##
        #TESTDEV0
        'ENTER 1ST IP HERE',
        #TESTDEV1
        'ENTER 2ND IP HERE',
        ]
##################################
##Commands list to be iterated through in function
##Commands listed are for Cisco ASA Firewalls
#ADD, CHANGE, OR REMOVE ANY COMMANDS THAT ARE NECESSARY FOR YOU
##################################
commands = [
        'en', + '\n',
        password + '\n',
        'terminal pager 0' + '\n' + '\n',
        'sh clock' + '\n' + '\n' + '\n' + '\n' + '\n' + '\n',
        'sh ver' + '\n' + '\n' + '\n' + '\n' + '\n' + '\n',
        'sh run access-group' + '\n' + '\n'+ '\n' + '\n' + '\n',
        'sh run' + '\n', 'exit' + '\n'
        ]
###############################
class ssh:
    client = None
    ###############################
    ##Function to create the folder
    ###############################
    def create_folder():
        if os.path.exists(CONFIGDIR):
            print "Path Exists Already @ " + CONFIGDIR
        elif not os.path.exists(CONFIGDIR):
            os.makedirs(CONFIGDIR)
            ##print "creating folder @ " + CONFIGDIR
    ###############################
    ##Initializing the class and creating the necessary components
    ###############################
    def __init__(self, address, username, password):
            ##print "Connecting to device."
            # Create a new SSH client
            self.client = paramiko.SSHClient()
            # The following line is required if you want the script to be able to access a device that's not yet in the known_hosts file
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # Make the connection
            self.client.connect(address, username=username, password=password, look_for_keys=False)
            ##print "Connected"
    ###############################
    ##sending the command list to the device
    ###############################
    def sendCommand(self, command):
        #Pausing before running the commands
        time.sleep(25)
        #invoking the ssh shell session
        chan = self.client.invoke_shell()
        #iterating through command list
        for command in commands:
            chan.send(command)
        ##print "sending commands"
        #creating a list to place the output in
        clientbuffer = []
        #this is used to get the entire output from the device
        try:
            while not chan.exit_status_ready():
                if chan.recv_ready():
                    data = chan.recv(4096)
                    while data:
                        clientbuffer.append(data)
                        data = chan.recv(4096)
        #joining the output to the list created above
            self.clientoutput = ''.join(clientbuffer)
            exit_status = chan.recv_exit_status()
        except:
            raise
        #closing the session
        self.client.close()
        ##print self.clientoutput
    ###############################
    ##Creating the files for each device configuration
    ###############################
    def TESTDEV0_File(self):
        #if file already exists, just print to the terminal
        if (path.isfile(TESTDEV0DIR)):
            print "File already exists @" + str(TESTDEV0DIR)
        #if no file exists, create it
        elif not(path.isfile(TESTDEV0DIR)):
            f = open(os.path.join(CONFIGDIR, TESTDEV0), 'w')
            with open(os.path.join(CONFIGDIR, TESTDEV0), 'w') as f:
                #write the device output to the file
                f.write('\n' + self.clientoutput)
                #close the file
                f.close
    def TESTDEV1_File(self):
        if (path.isfile(TESTDEV1DIR)):
            print "File already exists @" + str(TESTDEV1DIR)
        elif not(path.isfile(TESTDEV1DIR)):
            f = open(os.path.join(CONFIGDIR, TESTDEV1), 'w')
            with open(os.path.join(CONFIGDIR, TESTDEV1), 'w') as f:
                f.write('\n' + self.clientoutput)
                f.close
    ###############################
    ##Running the create folder function
    ###############################
    create_folder()
###############################
##Running the script for each host in the hosts list above
###############################
if __name__ == '__main__':
    TESTDEV0 = ssh(hosts[0], username, password)
    TESTDEV0.sendCommand(commands)
    TESTDEV0.TESTDEV0_File()

    TESTDEV1 = ssh(hosts[1], username, password)
    TESTDEV1.sendCommand(commands)
    TESTDEV1.TESTDEV1_File()

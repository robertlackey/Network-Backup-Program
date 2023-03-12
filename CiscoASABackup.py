import os
import paramiko
import datetime
import pwd
import grp
import getpass
import logging
from paramiko import client
from os import path
from datetime import datetime
from time import strftime, sleep
from multiprocessing import Pool

now = datetime.now()
day = now.strftime("%d")
month = now.strftime("%m")
TIMESTAMP = f'{now.year}{month}{day}'

CONFIGPATH = os.path.abspath("/home/")
CONFIGDIR = str(TIMESTAMP)

logging.basicConfig(filename=f"{CONFIGPATH}/{CONFIGDIR}/output.log", level=logging.INFO)

class ssh:
    def __init__(self, host, username, key_filename, commands):
        self.host = host
        self.username = username
        self.key_filename = key_filename
        self.commands = commands

    def sendCommand(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.host, username=self.username, key_filename=self.key_filename)
        logging.info(f"Connected to {self.host}")
        chan = client.invoke_shell()

        for command in self.commands:
            logging.info(f"Sending command: {command}")
            chan.send(command)

        clientbuffer = []
        try:
            while not chan.exit_status_ready():
                if chan.recv_ready():
                    data = chan.recv(10000)
                    while data:
                        clientbuffer.append(data)
                        data = chan.recv(4096)
            clientoutput = ''.join(clientbuffer)
        except Exception as e:
            logging.error(f"Error: {e}")
        finally:
            client.close()

        with open(os.path.join(CONFIGPATH, CONFIGDIR, f"{self.host.upper()}.txt"), 'w') as f:
            f.write(clientoutput)

def create_folder():
    if not os.path.exists(os.path.join(CONFIGPATH, CONFIGDIR)):
        os.makedirs(os.path.join(CONFIGPATH, CONFIGDIR))

def main():
    username = input("Enter Username: ")
    key_filename = input("Enter path to SSH private key: ")
    password = getpass.getpass("Enter passphrase for SSH private key: ")

    hosts = [
        #dev0
        'dev0',
        #dev1
        'dev1'
    ]

    commands = [
        'en\n',
        'terminal pager 0\n',
        'sh clock\n',
        'sh ver\n',
        'sh run access-group\n',
        'sh run\n', 
        'exit\n'
    ]

    create_folder()
    pool = Pool(processes=len(hosts))
    ssh_instances = [ssh(host, username, key_filename, commands) for host in hosts]
    pool.map(lambda x: x.sendCommand(), ssh_instances)
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()

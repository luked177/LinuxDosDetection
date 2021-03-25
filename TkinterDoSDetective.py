#Import Needed Libraries
import tkinter as tk
from tkinter import messagebox #messagebox
from scapy.all import *
from tkinter import simpledialog
import socket
import struct
import datetime
from PIL import ImageTk, Image

#Class for DoSDetective
class DoSDetective:

	def __init__(self): # Initialise Tkinter window app
		self.root = tk.Tk()
		self.root.title("DoS Detective") #Name the window
		self.root.geometry('500x200') #Size the window
		self._create_menubar() #Run create menubar function
		self.image_bck() #Run image background function

	def image_bck(self): #Create background image
		image1 = Image.open("DoSBck.png") #Import image
		image1 = image1.resize((500,200), Image.ANTIALIAS) #Resize image to match window size
		bck = ImageTk.PhotoImage(image1) #Create a photo image

		label1 = tk.Label(image=bck) #Add image to a label
		label1.image = bck

		label1.grid(column=0,row=0) # Position label

	def _create_menubar(self): #create the menu bar

		self.menubar = tk.Menu(self.root,background='#0B3D54', foreground='white', activebackground='#0B3D54', activeforeground='white')# Blue background to match background image, with white text
		self.root.configure(menu=self.menubar) #Configure the menubar

        # DoS menu
		DoSMenu = tk.Menu(self.menubar,tearoff=0) #Add the DoS Tab to menubar
		self.menubar.add_cascade(label="DoS Attack", menu=DoSMenu)
		DoSMenu.add_command(label="Start",command=self.startDoS) #Create a drop down that when clicked runs the startDos function

        # Detect DoS menu
		detectMenu = tk.Menu(self.menubar,tearoff=0) #Add the detect DoS to menubar
		self.menubar.add_cascade(label="Detect DoS", menu=detectMenu)
		detectMenu.add_command(label="Detect",command=self.detectDoS) #Run detectDoS function when clicked

        # Exit menu
		exitMenu = tk.Menu(self.menubar,tearoff=0) #Add exit to menubar
		self.menubar.add_cascade(label="Exit", menu=exitMenu)
		exitMenu.add_command(label="Exit", command=self.myExitApplication) #Run exit function created below


	def startDoS(self):#Function to start a DoS attack
		print("DoS Starting:") #Print to console for testing purposes
		src = simpledialog.askstring(title="Source IP",prompt="Enter IP address of Source: ") # Dialog box to get user input for source IP
		print("Source is: ",src) #Print to console for testing		
		target_IP = simpledialog.askstring(title="Target IP",prompt="Enter IP address of Target: ") # Dialog box to get user input for target IP
		print("Target is: ",target_IP)#Print to console for testing		
		i = 1 #Initialise variable i
		for source_port in range(1, 65535): #Send a packet to every port
			while i <= 25:	#Send 25 packets, not a true DoS but enough for testing purposes			
				IP1 = IP(src = src, dst = target_IP)
				TCP1 = TCP(sport = source_port, dport = 80)
				pkt = IP1 / TCP1
				send(pkt, inter = 0.5) # Send a packet every 0.5 seconds
				print ("packet sent ", i) # Tell command line that packet is sent for testing purposes
				i = i + 1 # Increase i
			break #After while loop. break from for loop
    
	def detectDoS(self):#Function to detect a DoS attack
		s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, 8)

		ipList = [] #Empty Array

		No_of_IPs = 15 # Set "abnormal" nuber of packets, it is 15 for testing purposes

		while True:
			pkt = s.recvfrom(2048) #Add packet recieved to variable
			ipheader = pkt[0][14:34] #Get IP header
			ip_hdr = struct.unpack("!8sB3s4s4s",ipheader) #Unpack IP header to calculate IP
			IP = socket.inet_ntoa(ip_hdr[3]) #Get IP using unpacked IP header

			ipList.append(IP)#Add IP to array
			if ipList.count(IP) > No_of_IPs:#If IP is in array more then number of abnormal IP packets
				print("DoS Detected")#Print for testing
				msgBox2 = messagebox.askquestion(title='DoS Detected', message='Warning: DoS Detected.\nSource:' + IP + '. \n Write IP to txt file?',icon="warning")#Warn user a DoS is detected, and ask if they would like a text file with info
				if msgBox2 == 'yes':#If user wants text file
					file_txt = open("attack_DoS.txt", 'a')#Open/Create a txt file
					t1 = datetime.datetime.now()+datetime.timedelta(hours=4)#Get gmt time
					t1 = t1.strftime("%c")#Format correctly
					t1 = str(t1)#Make a string

					file_txt.writelines(t1)#Write the date and time to textfile
					file_txt.writelines("\n")#Newline				
					line = "DOS Attack Detected: "
					file_txt.writelines(line)#Add line variable to text file
					file_txt.writelines(IP)#Write IP to textfile
					file_txt.writelines("\n")
					print("Writing to text file")#testing print
					break
				else:
					break
			else:
				continue

	def myExitApplication(self):
		MsgBox = messagebox.askquestion('Exit App', 'Are you sure?')#Ask if user wants to quit
		if MsgBox == 'yes': # If answer yes
			self.root.destroy() #Destroy Window

app = DoSDetective()#Run class DoSDetective
tk.mainloop()#Tkinter loops forever until interrupted
from faker import Faker
from random import randint
from cleverwrap import CleverWrap
from tkinter import *
import urllib
import tkinter as tk
import os

fake  = Faker()

# print (fake.name())
gend = 0	#0=male		1=female
dob =""
url = ""

root=Tk()
root.title("faker_formfilling")
root.geometry('500x200')
url1=tk.StringVar()
count=tk.IntVar()
count.set(1)
titleLabel=tk.Label(root,text="FAKE a FORM ")
titleLabel.grid(row=1,column=1)
urlLabel=tk.Label(root,text="FORM URL")
urlLabel.grid(row=3,column=5)
urlentry=tk.Entry(root,textvariable=url1,bg='#FFFFFF', fg='black')
urlentry.grid(row=3,column=10)
countLabel=tk.Label(root,text="NO OF TIMES ")
countLabel.grid(row=10,column=5)
countentry=tk.Entry(root,textvariable=count,bg='#FFFFFF', fg='black')
countentry.grid(row=10,column=10)


role=['listitem','radiogroup','radio','group','checkbox', 'listbox','option','combobox',  	'alert','button','presentation','list','heading']

def nextAlert(htm,tm):
    return htm.find('role="alert"',tm)

def countRadio(htm,tm):
    count=0
    mm=nextAlert(htm,tm)
    tm=htm.find('role="radio"',tm)
    while tm<mm:
   	 
   	 count=count+1
   	 tm=htm.find('role="radio"',tm)
   	 if(tm==-1):
   		 break
   	 tm=tm+1
    return count-1
def countGroup(htm,tm):
    count=0
    mm=nextAlert(htm,tm)
    tm=htm.find('role="checkbox"',tm)
    while tm<mm:
   	 # print mm
   	 # print tm
   	 
   	 count=count+1
   	 tm=htm.find('role="checkbox"',tm)
   	 if(tm==-1):
   		 break
   	 tm=tm+1
    return count-1
def countList(htm,tm):
    count=0
    mm=nextAlert(htm,tm)
    tm=htm.find('role="option"',tm)
    while tm<mm:
   	 
   	 count=count+1
   	 tm=htm.find('role="option"',tm)
   	 if(tm==-1):
   		 break
   	 tm=tm+1
    return count-1


def getQuestion(urlt):
    resp = urllib.request.urlopen(urlt)
    html = resp.read()
    html=html.decode('ASCII')
    question=list()
    # print(html)
    temp=0
    while temp!=-1:
   	 temp=html.find('role="heading"',temp)
   	 if(temp==-1):
   		 break
   	 # print(temp)
   	 for i in range(1000):
   		 if(html[temp]=='>'):
   			 temp=temp+1
   			 break;
   		 temp=temp+1
   	 str=""
   	 for i in range(1000):
   		 if(html[temp]=='<'):
   			 question.append(str)
   			 # print(str)
   			 str=""
   			 break
   		 else:
   			 str=str+html[temp]
   		 temp=temp+1
   	 temp=temp+1
    del question[0]
    return question

def getEntry(urlt):
	response = urllib.request.urlopen(urlt)
	html = response.read()
	html=html.decode('ASCII')
	question=list()
	# print(html)
	temp=0
	while temp!=-1:
		temp=html.find('"entry',temp)
		if(temp==-1):
			break
		# print(temp)
		temp=temp+1
		str=""
		for i in range(1000):
			if(html[temp]=='"'):
				question.append(str)
				print(str)
				str=""
				break
			else:
				str=str+html[temp]
			temp=temp+1
		temp=temp+1
	# del question[0]
	return question


def getType(url):
    resp = urllib.request.urlopen(url)
    html = resp.read()
    html=html.decode('ASCII')
    ques_type=list()
    # print(html)
    temp=0
    while temp!=-1:
   	 temp=html.find('role="heading"',temp)
   	 if(temp==-1):
   		 break
   	 temp=temp+6
   	 # print(temp)
   	 temp2=temp
   	 while temp2!=-1:
   		 temp2=html.find('role',temp2)
   		 if(temp2==-1):
   			 break
   		 temp2=temp2+6
   		 str=""
   		 for i in range(1000):
   			 if(html[temp2]=='"'):
   				 
   				 if(str=="alert" or str=="combobox"):
   					 
   					 ques_type.append(0)
   					 
   				 elif(str=="radiogroup"):
   					 
   					 t=temp2
   					 ques_type.append(0-countRadio(html,t))
   					 
   				 elif(str=="group"):
   					 
   					 t=temp2
   					 ques_type.append(countGroup(html,t))
   					 
   				 elif(str=="listbox"):
   					 
   					 t=temp2
   					 ques_type.append(0-countList(html,t))
   					 
   				 else:
   					 
   					 ques_type.append(1)
   					 
   				 
   				 str=""
   					 
   				 break
   			 else:
   				 str=str+html[temp2]
   			 temp2=temp2+1

   		 break
   	 temp=temp+1
    temp=temp+1
    del ques_type[0]
    return ques_type

def filePrint(res,url,entry):
	fh = open("ptoj.txt", "w")
	lines_of_text = [url+"\n"]
	fh.writelines(lines_of_text)
	for i in range(0,len(res)):
		lines_of_text = [entry[i]+"\n"]
		fh.writelines(lines_of_text)

		lines_of_text = [str(res[i])+"\n"]
		fh.writelines(lines_of_text)

	lines_of_text = ["#\n"]
	fh.writelines(lines_of_text)
	lines_of_text = ["#\n"]
	fh.writelines(lines_of_text)
	fh.close()


def theFunc(url):
	ques = getQuestion(url)
	typ = getType(url)
	res = select(ques,typ)
	ent = getEntry(url)
	print(res)
	print(ent)
	filePrint(res,url,ent)
	os.system("java submit")



def callAI(msg):
	cw = CleverWrap("CC8e31EaiwH16_bIY62-b0FesWw")
	return cw.say("You" + msg+ "?")
	# cw.reset()

# z = callAI("You Opinion on presendtial election?")
# print("TEST    "+z)



def select(ques, type):
	reply = ['']*len(type)
	print(len(reply))
	for i in range(0,len(type)):
		if(type[i]==0 ):
			reply[i]=response(ques[i])
		
		elif(type[i]>0):
			if(ques[i].find("gender")>-1):
				reply[i] = gend
			else:
				reply[i] = randint(0,int(type[i])-1)

		elif(type[i]<0):
			num = randint(1,mod(int(type[i])))
			s = set()
			for j in range(0,num):
				s.add(randint(0,mod(int(type[i]))-1))
			res = ""
			for j in s:
				res = res+str(j)+"#"
			reply[i] = res[:-1]

	return reply

def mod(num):
	if(num>=0):
		return num
	else :
		return 0-num


def response(msg):
	if (msg.lower().find("first nam")>-1):
		num = randint(1,10)
		if(num<=5):
			gend = 0
			return fake.first_name_male()
		else:
			gend =1
			return fake.first_name_female()
	
	elif msg.lower().find("last nam")>-1:
		return fake.last_name_female()
	
	elif msg.lower().find("name")>-1:
		num = randint(1,10)
		if(num<=5):
			gend = 0
			return fake.name_male()
		else:
			gend =1
			return fake.name_female()
	
	elif msg.lower().find("age")>-1:
		dob = fake.date('%Y-%m-%d')
		age = 2018-int(dob[0:dob.find('-')])
		print (dob)
		return age
	
	elif msg.lower().find("company")>-1:
		return fake.company()
	
	elif msg.lower().find("email")>-1:
		return fake.email()
	
	elif msg.lower().find("phone")>-1:
		return randint(734000000,999430000)
	
	elif msg.lower().find("income")>-1:
		return randint(2000,999999)
	
	elif msg.lower().find("addr")>-1:
		return fake.address()
	
	elif msg.lower().find("dob")>-1:
		return dob
	
	# elif msg.lower().find("gender")>-1:
	# 	return gend
	
	else :
		return callAI(msg)


def connectinternet():
    url=url1.get()
    c = count.get()

    # print(url1)
    # req = urllib.request.urlopen(url)
    # # connection=urllib.urlopen(req)
    # output=req.read()
    # print(output)
    for i in range(0,c):
    	theFunc(url)
    # req.close()

submitButton=tk.Button(root,text="submit",command=connectinternet)
submitButton.grid(row=50,column=30)
root.mainloop()


def response(msg):
	if (msg.lower().find("first nam")>-1):
		num = randint(1,10)
		if(num<=5):
			gend = 0
			return fake.first_name_male()
		else:
			gend =1
			return fake.first_name_female()
	
	elif msg.lower().find("last nam")>-1:
		return fake.last_name_female()
	
	elif msg.lower().find("name")>-1:
		num = randint(1,10)
		if(num<=5):
			gend = 0
			return fake.name_male()
		else:
			gend =1
			return fake.name_female()
	
	elif msg.lower().find("age")>-1:
		dob = fake.date('%Y-%m-%d')
		age = 2018-int(dob[0:dob.find('-')])
		print (dob)
		return age
	
	elif msg.lower().find("company")>-1:
		return fake.company()
	
	elif msg.lower().find("email")>-1:
		return fake.email()
	
	elif msg.lower().find("phone")>-1:
		return randint(734000000,999430000)
	
	elif msg.lower().find("income")>-1:
		return randint(2000,999999)
	
	elif msg.lower().find("addr")>-1:
		return fake.address()
	
	elif msg.lower().find("dob")>-1:
		return dob
	
	# elif msg.lower().find("gender")>-1:
	# 	return gend
	
	else :
		return callAI(msg)

# import urllib
# from urllib.request import urlopen
# from urllib2 import urlopen

# url='https://docs.google.com/forms/d/e/1FAIpQLSdr_QFf9-9x7vZTdCsh6F9tMAEvftr3hWpJmNnnrELafZmhUw/viewform?usp=sf_link'


# print getType(url)
# print getQuestion(url)








# print(response("name"))

# print(response(" last name "))
# print( response("age"))

# z = ""
def callAI(msg):
	cw = CleverWrap("CC8e31EaiwH16_bIY62-b0FesWw")
	return cw.say("You" + msg+ "?")
	# cw.reset()

# z = callAI("You Opinion on presendtial election?")
# print("TEST    "+z)



def select(ques, type):
	reply = ['']*len(type)
	print(len(reply))
	for i in range(0,len(type)):
		if(type[i]==0 ):
			reply[i]=response(ques[i])
		
		elif(type[i]>0):
			if(ques[i].find("gender")>-1):
				reply[i] = gend
			else:
				reply[i] = randint(0,int(type[i])-1)

		elif(type[i]<0):
			num = randint(1,mod(int(type[i])))
			s = set()
			for j in range(0,num):
				s.add(randint(0,mod(int(type[i]))-1))
			res = ""
			for j in s:
				res = res+str(j)+"#"
			reply[i] = res[:-1]

	return reply

def mod(num):
	if(num>=0):
		return num
	else :
		return 0-num

# que = ["first name","name","age","email","gender","Opinion on politics"]
# typ = [0,0,0,0,-5,0]

# print(select(que,typ))

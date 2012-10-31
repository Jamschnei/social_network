#!/usr/bin/python

__author__="shivekkhurana"
__version__="01.21.july.2010 || read as version.day.month.year"



from beaker.middleware import SessionMiddleware
from uuid import uuid1
from datetime import timedelta

import bottle
import sqlite3
import re



connection = sqlite3.connect('database.sqlite',check_same_thread=False)
database   = connection.cursor()

#/-----------------------------------#
#test
allFunc={'signup()':'done','signin()':'','signout()':'','addFriend()':'','removeFriend()':'',
'chat()':'','uploadPhoto()':'','removePhoto()':'','commentPhoto()':''}

#/-----------------------------------#

#staticFiles
@bottle.route('static/:filename')
def index():
	return bottle.static_file(filename,root='static')
	
#/-----------------------------------#

#signup
@bottle.get('/signup')
def index():
	return bottle.template('signup',bubbleMessage=':)')

@bottle.post('/signup')
def index():
	userid   = str(uuid1())
	username = bottle.request.forms.get('username').lower()
	email    = bottle.request.forms.get('email').lower()
	password = bottle.request.forms.get('password').lower()	

	checkUsername  = database.execute('''SELECT username FROM loginInfo WHERE username = ? ''',[username]) #check whether username already exists 
	usernameCheck  = database.fetchall()
	usernameCheck2 = username.split() #check whether username contain spaces
	
	checkEmail = database.execute('''SELECT email FROM loginInfo WHERE email = ? ''',[email]) #check whether email is already in use 
	emailCheck = database.fetchall()
	
	passwordCheck = password.split()
	
	reservedNames = ['signin','signup','signout','addFriend','removeFriend','chat','uploadPhoto','removePhoto','commentPhoto','static']
	
	errorMessage = ["my dear, this username is already in use. Sorry","dear -- username musn't have spaces in between.",
					"dear -- password musn't have spaces in between.","password too small,username already in use. Sorry",
					"password too small,email already in use. damn. sorry.","password too small,username and email already in use.",
					"baby, username should be 5 characters or more.","whoaa! , this email is already in use. sorry",
					"password too small.","that username is reserved"]
	
	if usernameCheck:	
		return bottle.template('signup',bubbleMessage = errorMessage[0])
		
	elif len(usernameCheck2)>1:	
		return bottle.template('signup',bubbleMessage = errorMessage[1])		
		
	elif len(passwordCheck) >1:	
		return bottle.template('signup',bubbleMessage=errorMessage[2])
		
	#compound conditions
	elif usernameCheck and len(password) <=6:
		return bottle.template('signup',bubbleMessage=errorMessage[3])
	
	elif emailCheck and len(password) <=6:
		return bottle.template('signup',bubbleMessage=errorMessage[4])
	
	elif usernameCheck and emailCheck and len(password) <=6:
		return bottle.template('signup',bubbleMessage=errorMessage[5])
	
	#normal conditions
	elif len(username) <4:
		return bottle.template('signup',bubbleMessage=errorMessage[6])
	
	elif emailCheck:
		return bottle.template('signup',bubbleMessage=errorMessage[7])
	
	elif len(password) <=6:
		return bottle.template('signup',bubbleMessage=errorMessage[8])
		
	elif reservedNames.__contains__(username):
		return bottle.template('signup',bubbleMessage=errorMessage[9])
		
	#finally make signup
	else:
		if len(email) > 7:
			if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
				loginInfo=(userid,username,email,password)
				database.execute('''INSERT INTO loginInfo VALUES(?,?,?,?)''',loginInfo) 
				database.execute('''INSERT INTO userInfo(userid) VALUES(?)''',[userid])
				connection.commit()
		else:
			return bottle.template('signup',bubbleMessage="email id invalid :(")
	signin(username,password)
#end:signup

#/-----------------------------------#

#signin
@bottle.get('/signin')
def index():
	return bottle.template('signin',bubbleMessage=':)')

@bottle.post('/signin')
def index(): 
	user=bottle.request.forms.get('user').lower()
	password=bottle.request.forms.get('password').lower()
	
	signinInfo = (user,user,password)
	
	verifySignin = database.execute('''SELECT userid FROM loginInfo WHERE (username = ? or email = ?)  AND password = ?''',signinInfo)
	getUserId = database.fetchone()
	
	fetchedUserId = getUserId #i.e the user id sent by the database
	if fetchedUserId:
		sessionStart(fetchedUserId)
		
	else:
		return bottle.template('signin',bubbleMessage='Hey, you entered invalid login info :/')
#end:signin

#/-----------------------------------#

#homepage

#>session manager
def sessionStart(sessionId):
	session_opts = {
	'session.auto'           : True,
	'session.cookie_domain'  : '/home',
	'session.cookie_expires' : timedelta(hours = 2),
	'session.type'           : 'file',
	'session.key'            : sessionId		
	}
	return True
	app = SessionMiddleware(bottle.app(), session_opts) 

@bottle.route('/home',method="GET")
def index():
	return "Success"	
	s = bottle.request.environ.get('beaker.session')
	s['test'] = s.get('test',0) + 1
	s.persist()
	return 'Test counter: %d' % s['test']
	
		

bottle.debug(True)
bottle.run(reloader = True)




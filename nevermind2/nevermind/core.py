#!/usr/bin/python

__author__="shivekkhurana"
__version__="01.21.july.2010 || read as version.day.month.year"



from uuid import uuid1

import bottle,sqlite3,hashlib,time,re

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

	checkUsername  = database.execute('''SELECT username FROM authInfo WHERE username = ? ''',[username]) #check whether username already exists 
	usernameCheck  = database.fetchall()
	usernameCheck2 = username.split() #check whether username contain spaces
	
	checkEmail = database.execute('''SELECT email FROM authInfo WHERE email = ? ''',[email]) #check whether email is already in use 
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
				authInfo = (userid,username,email,password)
				database.execute('''INSERT INTO authInfo VALUES(?,?,?,?)''',authInfo) 
				userData = (userid,username)
				database.execute('''INSERT INTO userData(userid,username) VALUES(?,?)''',userData)
				connection.commit()
		else:
			return bottle.template('signup',bubbleMessage="email id invalid :(")
	bottle.redirect('/signin')
#end:signup

#/-----------------------------------#

#signin
@bottle.get('/signin')
def index():
	if bottle.request.get_cookie('_aok_'):
		bottle.redirect('/home')
	else:
		return bottle.template('signin',bubbleMessage=':)')

@bottle.post('/signin')
def index(): 
	user=bottle.request.forms.get('user').lower()
	password=bottle.request.forms.get('password').lower()
	
	signinInfo = (user,user,password)
	
	verifySignin = database.execute('''SELECT userid FROM authInfo WHERE (username = ? OR email = ?)  AND password = ?''',signinInfo)
	userId = str(database.fetchone())
	
	if userId:
		sessionId = hashlib.sha224(str(time.time())).hexdigest()
		sessionSet = (sessionId,userId)
		database.execute('''UPDATE userData SET sessionId = ? WHERE userId = ?''',sessionSet)
		connection.commit()
		bottle.response.set_cookie('_aok_', sessionId, expires = 60 *60 * 2)
		bottle.redirect('/home')
	else:
		return bottle.template('signin',bubbleMessage='Hey, you entered invalid login info :/')
#end:signin

#/-----------------------------------#

#homepage
@bottle.route('/home',method="GET")
def index():	
	auth = bottle.request.get_cookie('_aok_')
	if auth:
		database.execute('''SELECT * FROM userData WHERE sessionId = ?''',[auth])
		results = database.fetchone()
		return str(results)
		
	else :
		return "You need to be logged in"
	
		

bottle.debug(True)
bottle.run(reloader = True)




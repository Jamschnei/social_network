#!/usr/bin/python

__author__="shivekkhurana"
__version__="01.21.july.2010 || read as version.day.month.year"



from uuid import uuid1

import bottle,hashlib,time,re,sqlite3,string,random

connection = sqlite3.connect('database.sqlite',check_same_thread = False)
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
#database functions

def checkNull(row):
	if row == None:
		return True
	else:
		return False
		
def fetchOne(columnName,table,reference,referenceValue):
	sql = '''SELECT %s FROM %s WHERE %s = '%s' '''%(columnName,table,reference,referenceValue)
	database.execute(sql)
	fetch = database.fetchone()
	return fetch[0]
	
def fetchElse(columns,table,reference,referenceValue):
	sql = '''SELECT %s FROM %s WHERE %s = '%s' '''%(columns,table,reference,referenceValue)
	database.execute(sql)
	fetch = database.fetchone()
	return fetch

def fetchAsList(columnName,table,reference,referenceValue):
	sql = '''SELECT %s FROM %s WHERE %s = '%s' '''%(columnName,table,reference,referenceValue)
	database.execute(sql)
	fetch = database.fetchone()
	if checkNull(fetch) != True:
		fetchedList = fetch[0].split()
		return fetchedList
	else:
		fetchedList = ''.split()
		return fetchedList
		
def convertToList(string):
	return string.split()
	
def update(tableName,columnName,newValue,refrence,referenceValue):
	sql = '''UPDATE %s SET %s = '%s' WHERE %s = '%s' '''%(tableName,columnName,newValue,refrence,referenceValue)
	database.execute(sql)
	connection.commit()

def returnAppend(nameOfList,value): #value = value to be added
	nameOfList.append(value)
	newList = ' '.join(nameOfList)
	return newList	
	
def returnDelete(nameOfList,value): #value = value to be deleted 
	nameOfList.remove(value)
	newList = ' '.join(nameOfList)
	return newList	
		
#simple functions

def requireAuth():
	if bottle.request.get_cookie('_aok_'):
		pass
	else:
		bottle.redirect('/authrequired')
		
def renewAuth():	
	sessionId = bottle.request.get_cookie('_aok_')
	bottle.response.set_cookie('_aok_', sessionId, expires = -1)
	bottle.response.set_cookie('_aok_', sessionId, expires = 60 * 60 * 2)
	
#/-----------------------------------#

#first page
@bottle.route('/')
def index():
	return bottle.template('signin',bubbleMessage = '')
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
	realName = bottle.request.forms.get('realName').lower()

	#check whether username already exists 
	usernameCheck  = fetchOne('username','authInfo','username',username)
	#check whether username contain spaces
	usernameCheck2 = username.split() #check whether username contain spaces
	
	#check whether email is already in use 
	emailCheck = fetchOne('email','authInfo','email',email)
 
	#check whether password contain spaces
	passwordCheck = password.split()
	
	reservedNames = ['signin','signup','signout','addFriend','removeFriend','chat','uploadPhoto',
					'removePhoto','commentPhoto','static','ads','settings','converse']
	
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
				userData = (userid,username,realName)
				database.execute('''INSERT INTO userData(userid,username,realName) 
									VALUES(?,?,? )''',userData)
				connection.commit()
		else:
			return bottle.template('signup',bubbleMessage="email id invalid :(")
	bottle.redirect('/signin')
#end:signup

#/-----------------------------------#
#Cookie Abbrevations
#====================
#_aok_ : authentication ok
#_aep_ : authentication expired
#_aaf_ : add as friend #set a cookie to fetch username of current url add as friend @route('/addfriend')
#_rdr_ : redirect

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
	userId = database.fetchone()
	
	if userId:
		sessionId = ''.join( [random.choice( string.letters + string.digits ) for i in range( 36 )] )
		sessionSet = (sessionId,userId[0])
		update('userData','sessionId',sessionId,'userId',userId[0])
		update('userData','status','online','userId',userId[0])

		bottle.response.set_cookie('_aok_', sessionId, expires = 60 * 60 * 2)
		bottle.redirect('/home')
	else:
		return bottle.template('signin',bubbleMessage='Hey, you entered invalid login info :/')
#end:signin

#signout
@bottle.route('/signout')
def index():
	requireAuth()
	userId = fetchOne('userId','userData','sessionId',bottle.request.get_cookie('_aok_'))

	update('userData','sessionId','NULL','userId',userId)
	update('userData','status','NULL','userId',userId)

	bottle.response.set_cookie('_aok_','',expires = -1)
	bottle.response.set_cookie('_aep_','lasso',expires = 2*60)
	if bottle.request.get_cookie('_aaf_'):
		bottle.response.set_cookie('_aaf_','',expires = -1)
	bottle.redirect('/home')

#end:signout

#/-----------------------------------#

#homepage
@bottle.route('/home',method="GET")
def index():	
	auth = bottle.request.get_cookie('_aok_')
	
	if auth:
		result = fetchElse('sessionId,username,realName,aboutMe,friends,friendRequests,photos','userData','sessionId',auth)
		friends = fetchOne('friends','userData','sessionId',auth)
		if friends:
			f = converToList(friends)
		else:
			f = []
			
		friendRequests = fetchOne('friendRequests','userData','sessionId',auth)
		if friendRequests:
			fr = converToList(friends)
		else:
			fr = []
		
		return bottle.template('home', f =f, fr = fr, realName = result[2],aboutMe = result[3] )
	elif bottle.request.get_cookie('_aep_'):
		bottle.redirect('/')
		
#add as friend
@bottle.route('/addfriend')
def index():
	requireAuth()
	if bottle.request.get_cookie('_aaf_'):
		friend           = bottle.request.get_cookie('_aaf_')
		currentSessionId = bottle.request.get_cookie('_aok_')
		current = fetchOne('username','userData','sessionId',currentSessionId)
		friendList = fetchAsList('friendRequests','userData','username',friend)
		update('userData','friendRequests',returnAppend(friendList,current),'username',friend)

		return bottle.template('home',bubble = "Request Sent to %s" % (friend), row = fetchElse('*','userData','sessionId',currentSessionId))
		bottle.response.set_cookie('_aaf_','',expires = -1)
	else:	
		return "go back to previous page and visit again" ###bottle.redirect('/cookie-timeout')
		
@bottle.route('/accept/:username')
def index(username):
	requireAuth()
	currentSessionId = bottle.request.get_cookie('_aok_')
	requests = fetchAsList('friendRequests','userData','sessionId',currentSessionId)
	if requests.__contains__(username):
		#accept as friend
		currentFriends = fetchAsList('friends','userData','sessionId',currentSessionId)	
		final = returnAppend(currentFriends,username)
		update('userData','friends',final,'sessionId',currentSessionId)
	
		#delete request
		final = returnDelete(requests,username)
		update('userData','friendRequests',final,'sessionId',currentSessionId)
		
		bottle.redirect('/username')
	else:
		bottle.redirect('/home')
		
@bottle.route('/ignore/:username')
def index(username):
	requireAuth()
	currentSessionId = bottle.request.get_cookie('_aok_')
	requests = fetchAsList('friendRequests','userData','sessionId',currentSessionId)
	if requests.__contains__(username):
		final = returnDelete(requests,username)
		update('userData','friendRequests',final,'sessionId',currentSessionId)
		bottle.redirect('/username')
	else:
		bottle.redirect('/home')
#/-----------------------------------#

bottle.debug(True)
bottle.run(reloader = True)




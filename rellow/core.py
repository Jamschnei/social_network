#!/usr/bin/python

__author__="shivekkhurana"
__version__="02-2.24.August.2010   || read as version.day.month.year"

#Cookie Abbrevations
#====================
#_aok_ : authentication ok
#_aep_ : authentication expired
#_rmf_ : remove friend #set a cookie to fetch username of current url add remove friend @route('/removefriend')
#_rdr_ : redirect
#_bbm_ : bubbleMessage
#_unm_ : username
#_rmn_ : return to index page (return main)

#Conventions
#====================
#username is typed as username <-> exception
#real name as realName
#upper *S* means friend's stuff.


import bottle,hashlib,time,re,sqlite3,string,random,uuid

connection = sqlite3.connect('database.sqlite',check_same_thread = False)
database   = connection.cursor()

#/-----------------------------------#
#test
allFunc={'signup()':'done','signin()':'','signout()':'','addFriend()':'','removeFriend()':'',
'chat()':'','uploadPhoto()':'','removePhoto()':'','commentPhoto()':''}

#/-----------------------------------#

#cssFiles
@bottle.route('/css/:filename')
def send_static(filename):
    return bottle.static_file(filename, root='/media/workspace/rellow/')
	
#/-----------------------------------#
#database functions
		
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
	
def fetchAll(columns,table,reference,referenceValue):
	sql = '''SELECT %s FROM %s WHERE %s = '%s' '''%(columns,table,reference,referenceValue)
	database.execute(sql)
	fetch = database.fetchall()
	return fetch
	
def convertToList(string):
	return string.split()

def fetchAsList(columnName,table,reference,referenceValue):
	fetch = fetchOne(columnName,table,reference,referenceValue)
	if fetch:
		fetchedList = convertToList(fetch)
	else:
		fetchedList = []
	return fetchedList
	
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
		renewAuth()
	elif bottle.request.get_cookie('_aep_'):
		bottle.redirect('/')
	else:
		bottle.redirect('/authrequired')
			
def renewAuth():	
	sessionId = bottle.request.get_cookie('_aok_')
	bottle.response.set_cookie('_aok_', sessionId, expires = -1,path = '/')
	bottle.response.set_cookie('_aok_', sessionId, expires = 60 * 60 * 2,path = '/')
	
def deleteCookie(cookie):
	if bottle.request.get_cookie(cookie):
		bottle.response.set_cookie(cookie,'',expires=-1,path="/")
	
def redirect(cookie,path):
	if bottle.request.get_cookie(cookie):
		deleteCookie(cookie)
		bottle.redirect(path)
	
def getUserId(reference,val):
	return fetchOne('userId','userData',reference,val)

def getUserName(reference,val):
	return fetchOne('username','userData',reference,val)
	
def getRealName(reference,val):
	return fetchOne('realName','userData',reference,val).replace('_',' ')
	
def getSid(reference,val):
	return fetchOne('sessionId','userData',reference,val)
	
#form/cookie functions

def getFormValue(field):
	return bottle.request.forms.get(field)
	
def getCookie(cookieName):
	return bottle.request.get_cookie(cookieName)
	
#/-----------------------------------#

#first page
@bottle.route('/')
def index():
	redirect('_aok_','/home')
	if bottle.request.get_cookie('_aep_'):
		deleteCookie('_aep_')
	return bottle.template('signin',bubbleMessage = '')
	
#/-----------------------------------#
#signup
@bottle.get('/signup')
def signupGet():
	if bottle.request.get_cookie('_aok_'):
		bottle.redirect('/home')
	return bottle.template('signup',bubbleMessage='')

@bottle.post('/signup')
def signupPost():
	userid   = str(uuid.uuid1())
	username = bottle.request.forms.get('username').lower()
	email    = bottle.request.forms.get('email').lower()
	password = bottle.request.forms.get('password').lower()	
	realName = '_'.join(bottle.request.forms.get('realName').lower().split())

	#check whether username already exists 
	usernameCheck  = fetchElse('username','authInfo','username',username)
	#check whether username contain spaces
	usernameCheck2 = username.split() #check whether username contain spaces
	
	#check whether email is already in use 
	emailCheck = fetchElse('email','authInfo','email',email)
 
	#check whether password contain spaces
	passwordCheck = password.split()
	
	reservedNames = ['signin','signup','signout','addFriend','removeFriend','chat','uploadPhoto',
					'removePhoto','commentPhoto','static','ads','settings','converse','-']
	
	errorMessage = ["my dear, this username is already in use. Sorry",
					"dear -- username musn't have spaces in between.",
					"dear -- password musn't have spaces in between.",
					"password too small,username already in use. Sorry",
					"password too small,email already in use. damn. sorry.",
					"password too small,username and email already in use.",
					"baby, username should be between 3 - 20 characters (no spaces)",
					"whoaa! , this email is already in use. sorry",
					"password too small.",
					"that username is reserved",
					"email doesn't looks to be ok."]
	
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
	elif len(username) <3 or len(username) > 20:
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
									VALUES(?,?,?)''',userData)
				database.execute('''INSERT INTO settingData(userid) 
									VALUES(?)''',[userData[0]])
				connection.commit()
				signin(username,password)
			else:
				return bottle.template('signup',bubbleMessage=errorMessage[10])
		else:
			return bottle.template('signup',bubbleMessage = errorMessage[10])
#end:signup

#/-----------------------------------#

#signin

def signin(user,password): 
	signinInfo   = (user,user,password)
	verifySignin = database.execute('''SELECT userid FROM authInfo WHERE (username = ? OR email = ?)  AND password = ?''',signinInfo)
	userId       = database.fetchone()
	if userId:
		sessionId  = ''.join( [random.choice( string.letters + string.digits ) for i in range( 36 )] )
		sessionSet = (sessionId,userId[0])
		update('userData','sessionId',sessionId,'userId',userId[0])
		update('userData','status','online','userId',userId[0])
		bottle.response.set_cookie('_aok_', sessionId, expires = 60 * 60 * 2, path='/')
		bottle.redirect('/home')
	else:
		return bottle.template('signin',bubbleMessage='Hey, you entered invalid login info ')
		
@bottle.get('/signin')
def signinGet():
	if bottle.request.get_cookie('_aok_'):
		bottle.redirect('/home')
	else:
		return bottle.template('signin',bubbleMessage='')

@bottle.post('/signin')			
def signinPost():
	user     = bottle.request.forms.get('user').lower()
	password = bottle.request.forms.get('password').lower()
	return signin(user,password)
#end:signin

#signout
@bottle.route('/signout')
def signout():
	requireAuth()
	deleteCookie('_rdr_')
	userId = fetchOne('userId','userData','sessionId',bottle.request.get_cookie('_aok_'))
	update('userData','sessionId','NULL','userId',userId)
	update('userData','status','NULL','userId',userId)
	deleteCookie('_aok_')
	bottle.response.set_cookie('_aep_','lasso',expires = 2*60 , path = '/')
	if bottle.request.get_cookie('_unm_'):
		deleteCookie('_unm_')
	bottle.redirect('/home')
#end:signout

#/-----------------------------------#
#homepage
@bottle.route('/home',method="GET")
def home():	
	redirect('_aep_','/') # when signed out, this will redirect to main page @route('/')
	requireAuth()
	auth = bottle.request.get_cookie('_aok_')
	result = fetchElse('sessionId,username,realName,aboutMe,friends,friendRequests,photos','userData','sessionId',auth)
	friendList = {}
	for friend in fetchAsList('friends','userData','sessionId',auth):
		friendList[getUserName('userId',friend)] = getRealName('userId',friend)
	friendRequests = {}
	for request in fetchAsList('friendRequests','userData','sessionId',auth):
		friendRequests[getUserName('userId',request)] = getRealName('userId',request) 
	realName = result[2].replace('_',' ') 
	if result[3]: aboutMe = result[3]
	else: aboutMe = ''
	return bottle.template('home',
					friendList      = friendList,
					friendRequests  = friendRequests, 
					realName        = realName,
					aboutMe         = aboutMe,
					currentUserName = getUserName('sessionId',auth),
					friendsOnline	= 0 #TODO
					)
		
#settings
@bottle.get('/settings')
def settingsGet():
	redirect('_aep_','/')
	requireAuth()
	deleteCookie('_rdr_')
	current     = getUserId('sessionId',bottle.request.get_cookie('_aok_'))
	userData    = fetchElse('username,realName,aboutMe','userData','userId',current)
	settingData = fetchElse('location,favoriteStuff,website','settingData','userId',current)
	username    = userData[0]
	realName    = userData[1].replace('_',' ')
	if userData[2]: aboutMe = userData[2]
	else: aboutMe = ''
	friendList = {}
	for friend in fetchAsList('friends','userData','username',username):
		userSname = getUserName('userId',friend)
		realSName = getRealName('userId',friend) 
		friendList[userSname] = realSName
	if settingData[0]: location = settingData[0]
	else: location = ''
	if settingData[1]: favoriteStuff = settingData[1]
	else: favoriteStuff = ''
	if settingData[2]: website = settingData[2]
	else: website = ''
	return bottle.template('settings',
					username      = username,
					realName      = realName,
					aboutMe       = aboutMe,
					friendList    = friendList,
					location      = location,
					favoriteStuff = favoriteStuff,
					website       = website  
					)
					
@bottle.route('/setrmf/:username')
def setRemoveFriendCookie(username):
	bottle.response.set_cookie('_rmf_',username,expires=60*5,path='/')
	bottle.redirect('/%s'%(username))
				
@bottle.post('/settings')
def settingsSave():
	current      = getUserId('sessionId',bottle.request.get_cookie('_aok_'))
	userData     = fetchElse('username,realName,aboutMe,friends','userData','userId',current)
	settingData  = fetchElse('location,favoriteStuff,website','settingData','userId',current)
	updateDictUd = {} #ud = for userData
	updateDictSd = {} #sd = for settingData 
	username = bottle.request.forms.get('username')
	usernameCheck  = fetchElse('username','authInfo','username',username)
	usernameCheck2 = username.split() #check whether username contain spaces
	if username == userData[0]:pass
	elif usernameCheck:
		return "username already taken."
	elif len(usernameCheck2) > 1:
		return "baby, username musn't have spaces."
	else:
		updateDictUd['username'] = username
		update('authInfo','username',username,'userId',current)
	
	realName = bottle.request.forms.get('realName')
	if realName == userData[1]:pass
	else:updateDictUd['realName'] = realName
	
	aboutMe = bottle.request.forms.get('aboutMe')
	if realName == userData[2]:pass
	else:updateDictUd['aboutMe'] = aboutMe
	
	location = bottle.request.forms.get('location')
	if location == settingData[0]:pass
	else:updateDictSd['location'] = location
	
	favoriteStuff = bottle.request.forms.get('favoriteStuff')
	if favoriteStuff == settingData[1]:pass
	else:updateDictSd['favoriteStuff'] = favoriteStuff
					
	website = bottle.request.forms.get('website')
	if website == settingData[2]:pass
	else:updateDictSd['website'] = website
	
	for key,value in updateDictUd.items():
		update('userData',key,value,'userId',current)
	for key,value in updateDictSd.items():
		update('settingData',key,value,'userId',current)
	
	bottle.response.set_cookie('_bbm_','you account settings have been saved', path = "/", expires = 20)	
	bottle.redirect('/%s'%(username))

#profile
@bottle.route('/:username')
def profile(username):
	auth         = bottle.request.get_cookie('_aok_')
	info         = fetchElse('realName,aboutMe','userData','username',username) #profileSinfo
	settingData  = fetchElse('location,favoriteStuff,website','settingData','userId',getUserId('username',username)) #profileSsettingData
	deleteCookie('_unm_')
	bottle.response.set_cookie('_unm_',username,expires = 2400, path = '/')
	
	redirect('_rmf_','/removefriend')
	
	if info:
		if auth:
			currentUserId   = getUserId('sessionId',auth)
			currentUserName = getUserName('sessionId',auth)
		#/-----------------------------------#
		showAddFriend  = True 
		owner          = False
		hasRequestList = {}
		friend         = False
		hasRequested   = False
		request        = False	
		bubbleMessage  = ''
		addNote        = True
		allNotes       = {}
		#/-----------------------------------#
		if auth:
			if currentUserName == username: 
				owner          = True
				showAddFriend  = False
				addNote        = False
			else: owner        = False
		#/-----------------------------------#
		realName = info[0].replace('_',' ')
		if info[1]:aboutMe = info[1]
		else:aboutMe = ''
		#/-----------------------------------#			
		if auth:loggedIn = True
		else:
			loggedIn    = False
			bottle.response.set_cookie('_unm_',username,expires = 36000)
		#/-----------------------------------#
		friendList = {}
		for friend in fetchAsList('friends','userData','username',username):
			userSname = getUserName('userId',friend)
			realSName = getRealName('userId',friend) 
			friendList[userSname] = realSName
		#/-----------------------------------#	
		if auth:	
			for hasRequest in fetchAsList('friendRequests','userData','userId',currentUserId):
				username = getUserName('userId',hasRequest)
				realName = getRealName('userId',hasRequest) 
				hasRequestList[username] = realName
		#/-----------------------------------#		
		requestList = []
		for request in fetchAsList('friendRequests','userData','username',username):
			requestList.append(getUserName('userId',request))
			bubbleMessage =" Hey, this is your profile."
		#/-----------------------------------#
		if auth:
			if friendList.__contains__(currentUserName):
				friend        = True
				showAddFriend = False
			else:friend       = False
		#/-----------------------------------#
			if hasRequestList.__contains__(username):
				hasRequested  = True
				showAddFriend = False
			else:hasRequested = False
		#/-----------------------------------#
			if requestList.__contains__(currentUserName):
				request       = True
				showAddFriend = False
			else:request      = False			
		#/-----------------------------------#					
		bbm = bottle.request.get_cookie('_bbm_')
		if bbm:
			bubbleMessage = bbm 
		#/-----------------------------------#
		if settingData[0]:location = settingData[0]
		else:location = ''
		if settingData[1]:favoriteStuff = settingData[1]
		else:favoriteStuff = ''
		if settingData[2]:website = settingData[2]
		else:website = ''
		#/-----------------------------------#
		#notes
		if auth:
			compoundNotes = fetchAll('sender,toUserId,noteId,note,inReplyTo,fromUserId,fromEmail','notesData','toUserId',currentUserId)
			simpleNote    = fetchAll('note,sender','notesData','toUserId',currentUserId)
 			allNotes	  = dict(simpleNote)
		#/-----------------------------------#
		return bottle.template('profile' , 
						friendList    = friendList,
						realName      = realName, 
						aboutMe       = aboutMe,
						loggedIn      = loggedIn,
						friend        = friend, 
						request       = request, 
						hasRequested  = hasRequested,
						username      = username,
						showAddFriend = showAddFriend,
						owner         = owner,
						bubbleMessage = bubbleMessage,
						location      = location,
						favoriteStuff = favoriteStuff,
						website       = website,
						addNote       = addNote,
						allNotes      = allNotes
						)	
		
	else:
		return " user doesn't exist"
		
		
#addnote
@bottle.post('/addnote')
def addNote():
	#table structure -> sender,toUserId,noteId,note,inReplyTo,fromUserId,fromEmail
	note      = getFormValue('note')
	email     = getFormValue('email')
	noteId    = ''.join( [random.choice( string.letters + string.digits ) for i in range( 38 )] )
	toUserId  = getUserId('username',bottle.request.get_cookie('_unm_'))
	auth      = getCookie('_aok_')
	inReplyTo = None
	if auth:
		sender     = getUserName('sessionId',auth)
		fromUserId = getUserId('sessionId',auth)
		fromEmail  = None
	else:
		sender     = email
		fromEmail  = email
		fromUserId = None
		
	notesInfo = (sender,toUserId,noteId,note,inReplyTo,fromUserId,fromEmail)
	try:
		database.execute('''INSERT INTO notesData VALUES(?,?,?,?,?,?,?)''',notesInfo)
		connection.commit()
		return "Message sent"
	except:
		return "There was some problem, please try again."
		
#add as friend
@bottle.route('/addfriend')
def index():
	requireAuth()
	if bottle.request.get_cookie('_unm_'):
		friend            = getUserId('username' , bottle.request.get_cookie('_unm_'))
		current           = getUserId('sessionId',bottle.request.get_cookie('_aok_'))
		friendRequestList = fetchAsList('friendRequests','userData','userId',friend)
		update('userData','friendRequests',returnAppend(friendRequestList,current),'userId',friend)
		deleteCookie('_unm_')
		bottle.redirect('/%s'%(bottle.request.get_cookie('_unm_')))
	else:	
		return "go back to previous page and visit again" ###bottle.redirect('/cookie-timeout')
		
@bottle.route('/removefriend')
def removeFriend():
	requireAuth()
	fetchedUserName = bottle.request.get_cookie('_unm_')
	if getUserName:
		friend  = getUserId('username',fetchedUserName)
		current = getUserId('sessionId',bottle.request.get_cookie('_aok_'))
		update('userData','friends',returnDelete(fetchAsList('friends','userData','userId',friend),current),'userid',friend)
		update('userData','friends',returnDelete(fetchAsList('friends','userData','userId',current),friend),'userid',current)
		deleteCookie('_unm_')
		bottle.redirect('/%s'%(fetchedUserName))
	else:	
		return "go back to previous page and visit again" ###bottle.redirect('/cookie-timeout')

@bottle.route('/accept/:username')
def index(username):
	requireAuth()
	currentSessionId = bottle.request.get_cookie('_aok_')
	requests         = []
	for request in fetchAsList('friendRequests','userData','sessionId',currentSessionId):
		requests.append(getUserName('userId',request))
	
	friendSList      = []
	for friend in fetchAsList('friends','userData','username',username):
		friendSList.append(getUserName('userId',friend))
	
	if requests.__contains__(username):
		
		#accept as friend
		currentFriends = fetchAsList('friends','userData','sessionId',currentSessionId)	
		update('userData','friends',returnAppend(currentFriends,getUserId('username',username)),'sessionId',currentSessionId)
		update('userData','friends',returnAppend(friendSList,getUserId('sessionId',currentSessionId)),'username',username)
	
		#delete request
		update('userData','friendRequests',returnDelete(fetchAsList('friendRequests','userData','sessionId',currentSessionId)\
		,getUserId('username',username)),'sessionId',currentSessionId)
		bottle.redirect('/%s'%(username))
	else:
		bottle.redirect('/home')
		
@bottle.route('/ignore/:username')
def index(username):
	requireAuth()
	currentSessionId = bottle.request.get_cookie('_aok_')
	requests         = fetchAsList('friendRequests','userData','sessionId',currentSessionId)
	sUserId          = getUserId('username',username)
	if requests.__contains__(sUserId):
		final = returnDelete(requests,sUserId)
		update('userData','friendRequests',final,'sessionId',currentSessionId)
		bottle.redirect('/%s'%(username))
	else:
		bottle.redirect('/home')
#/-----------------------------------#

bottle.debug(True)
bottle.TEMPLATES.clear()
bottle.run(reloader = True)

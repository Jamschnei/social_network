from bottle import route, request, response,run,redirect,debug
@route('/')
def index():
	return 'logged out'
@route('/counter')
def counter():
    count = int( request.COOKIES.get('counter', '0') )
    count += 1
    response.set_cookie('counter', str(count))
    return '''You visited this page %d times <br/> <a href='/logout'>logout</a>''' % count
    
    
@route('/logout')
def logout():
	a = response.get_cookie('counter')
	del(a)
	redirect ('/')
	
debug(True)
run(reloader = True)

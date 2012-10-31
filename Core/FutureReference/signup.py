#user_maker.py 

__author__='''Shivek Khurana'''
__version__='''01.12.04.2010 | read as version.day.month.year''' 
__doc__='''Description : Create a dictionary named users, and add functionality to add, remove a user.'''
uname={'shivek':'shivekk@gmail.com','mehak':'mehak@ls.com'}

def username_input():
    '''New user ? add yourself to the list'''
    global u
    while True:
        u=input('username : ')
        if len(u)<=1:
            print('''invalid username :{''')
        elif uname.__contains__(u):
            print('''username already in use :(''')
        else:
            break          

def email_validator(email):
    import re
    if len(email) >=6:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            for a,b in uname.items():
                if email==b:
                    print('''email already in use :{''')
                    return email_input()
            print('''done''')         
        else:
            print('''email not valid :(''')
            return email_input()
    else:
        print('''invalid email :{''')
        return email_input()

def email_input():
    e=input('''email id : ''')
    email_validator(e)

def lister():
    for a,b in uname.items():
        print('''{0} : {1}'''.format(a,b))

def form():
    username_input()
    email_input()

form()
uname[u]=e

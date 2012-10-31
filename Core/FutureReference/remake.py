#signup.py

#-->STATUS : suspended as dict() cannot hold a [list] as a key value. (future reference.)


__author__='''Shivek Khurana'''
__version__='''1.9.5.2010 | read as version.day.month.year'''
__doc__='''create a user (if desired username is available{ask for a new username if not available}) check whether it already exists, raise error if it does, validate email id and length of password.'''

#-->UserCore = {[username,email]:password} || basic login information for all users. 
UserCore={}

def UsernameValidator(username):
    if len(username)<3:
        print('''username must be 3 characters or more.''')
        return signup()
    else:
        for a,b in UserCore.items():
            if a.__contains__(username):
                print('''username already taken''')
                return signup()
            else:
                print(username,''' - is really cool ;)''') 

def EmailValidator(email):
    import re
    if len(email)>=6:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email)!=None:
            pass                  
        else:
            print('''email invalid :{''')
            return signup()
    else:
        print('''email too short for us to believe it exists.''')
        return signup()
    for a,b in UserCore.items():
        if a.__contains__(email):
            print('''email already in use :(''')
            return signup()
        else:
            continue
        
def PasswordValidator(password):
    if len(password)<6:
        print('''password to short :/''')
           
def signup():
    u=input('''username (no fishy spaces!) : ''')
    UsernameValidator(u)
    e=input('''email id : ''')
    EmailValidator(e)
    p=input('''password (think cheeky) : ''')
    PasswordValidator(p)
    print('''user created, welcome to the family (you can enter your real name later in your profile)''')
    UserCore[u,e]=p
    #import os
    #os.mkdir("/home/shivekk/anyfolder"+u)
    
    
        

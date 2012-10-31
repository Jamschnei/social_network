UserCore={('shivekk@gmail.com','shivekk','SHIVEKK','Shivekk'):'lovebulls'}

def LoginFunc():
    x=input('''uname : ''')
    if len(x)<=5:
        print('''Username too fishy :P''')
    else:
        y=input('''pass : ''')
    for a,b in UserCore.items():
        if a.__contains__(x):
            if b==y:
                print('''logged in''')
            else:
                print('''My dear, you probably mistyped your password.''')
        else:
            print('''no such user, you probably mistyped it :}''')

LoginFunc()

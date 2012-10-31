<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>home</title>

    <!-- Framework CSS -->
    <link rel="stylesheet" href="/css/screen.css" type="text/css" media="screen, projection">
    <link rel="stylesheet" href="/css/print.css" type="text/css" media="print">
    <!--[if lt IE]><link rel="stylesheet" href="/css/ie.css" type="text/css" media="screen, projection"><![endif]-->
    <style type="text/css" media="screen">
      p, table, hr, .box { margin-bottom:25px; }
      .box p { margin-bottom:10px; }
    </style>
  </head>
  <body>
  	<div class="container">
  		<div class="span-5 append-1">
  		<ul>
			<li><a href = "/home" class = "">home</a></li>
			<!--<li><a href = "/converse" class = "">converse</a></li>-->
			<li><a href = "/favorites" class = "">favorites</a></li>
			<li><a href = "/{{currentUserName}}" class = "">profile</a></li>
			<hr/>
			<li>friends online : {{friendsOnline}}</li>
		</ul>
		<ul>
			%#friends
			%if len(friendList) != 0:
				<li>friends</li>
			%else:
				%pass
			%end
			%for uname,frnd in friendList.items():
			<li><a href = '/{{uname}}' title = "{{frnd}}">{{frnd}}</a></li>
			%end
		</ul>
		<ul>
			%#friend requests
			%if len(friendRequests) != 0:
				<li>friend requests</li>
			%else:
				%pass
			%end
			%for uname,req in friendRequests.items(): 
			<li><a href="/{{uname}}" title = "friend request from {{req}}" class = "quiet">{{req}}</a> -- 
			<a href="/accept/{{uname}}">accept</a> |
			<a href="/ignore/{{uname}}" class = "quiet">ignore</a></li>
			%end
		</ul>
		<ul>
			<li><a href = "/settings" class = "">settings</a></li>
			<!--<li><a href = "/log" class = "">chat log</a></li>-->
			<li><a href = "/signout" class = "">signout</a></li>
		</ul>
 	</div> 
 		
 		<div class="span-4" id="glassMessage">
 		Hello dear
 		</div>	
  	<div>
  </body>

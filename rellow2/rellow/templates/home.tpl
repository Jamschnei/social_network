<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Blueprint test pages</title>

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
			<li><a href = "/-/home" class = "quiet">home</a></li>
			<li><a href = "/-/converse" class = "quiet">converse</a></li>
			<li><a href = "/-/favorites" class = "quiet">favorites</a></li>
		</ul>
		<hr/>
		<ul>
			%#friends
			%for frnd in f:
			<li><a href = '/-/{{frnd}}' title = "{{frnd}}">{{f}}</a></li>
			%end
		</ul>
		<ul>
			%#friend requests
			%for req in fr: 
			<li><a href="/-/{{req}}" title = "friend request from {{req}}" class = "quiet">{{req}}</a> -- 
			<a href="/-//accept/{{req}}">accept</a> |
			<a href="/-/ignore/{{req}}" class = "quiet">ignore</a></li>
			%end
		</ul>
		<ul>
			<li><a href = "/-/settings" class = "quiet">settings</a></li>
			<li><a href = "/-/log" class = "quiet">chat log</a></li>
			<li><a href = "/-/signout" class = "quiet">signout</a></li>
		</ul>
 	</div> 
 		
 		<div class="span-4">
 		some lipsum
 		</div>	
  	<div>
  </body>

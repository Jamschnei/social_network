<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>home</title>

    <!-- Framework CSS -->
    <link rel="stylesheet" href="/css/screen.css" type="text/css" media="screen, projection">
    <script type="text/javascript" src="css/jquery.js"></script>
    <script src="css/jquery.jgrowl.js"></script>
    <link rel="stylesheet" type="text/css" href="css/jquery.jgrowl.css"/>
    <link rel="stylesheet" href="/css/print.css" type="text/css" media="print">
    <!--[if lt IE]><link rel="stylesheet" href="css/ie.css" type="text/css" media="screen, projection"><![endif]-->
    <style type="text/css" media="screen">
      p, table, hr, .box { margin-bottom:25px; }
      .box p { margin-bottom:10px; }
      
      .true{border:1px solid #489;}
    </style>    
    <script type="text/javascript">   
    	function favoritetoggle(noteContainerId)
		{	
			$.ajax({
			url: "/notes/favoritetoggle",
			type: "POST",
			data: {"noteId": noteContainerId},
			
			success: function(returnedValue){
				$('a#'+noteContainerId).text(returnedValue);
				}
			});
		}
    
    </script>
  </head>
  <body>
  	<div class="container">
  		<div class="span-5 append-1">
  		<ul>
			<li><a href = "/home" class = "">home</a></li>
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
 	
 		<div id="notesContainer" class="span-12 last" style="border:1px solid #999;padding:20px;">
		%for noteInfo in allNotes:
		%if noteInfo[3] == False:
		<div class="note">
			<span class="sender">{{noteInfo[0]}}</span> ->
			<span class="body">{{noteInfo[1]}}</span>
			<div class="noteOptions">
			%if noteInfo[4]:
				<a href="/notes/favoritetoggle" id = "{{noteInfo[2]}}"  onClick="favoritetoggle('{{noteInfo[2]}}');return false;" 
				class="favoritetoggle">remove</a> |
			%else:
				%#that means note is not in the favorites list			
				<a href="/notes/favoritetoggle" id = "{{noteInfo[2]}}"  onClick="favoritetoggle('{{noteInfo[2]}}');return false;"  
				class="favoritetoggle">favorite</a> |
			%end
				<a href="/notes/block/{{noteInfo[2]}}" name = "block" id = "block">block this person</a> |
				<a href="/notes/close/{{noteInfo[2]}}" name = "close" id = "close">close</a> |
				<a href="/notes/reply/{{noteInfo[2]}}" name="reply" id = "reply">reply</a> 
			</div>
		</div>
		%end
		%end
		</div>
  	<div>
  </body>

<!DOCTYPE html PUBLIC '-//W3C//DTD HTML 4.01//EN'
   'http://www.w3.org/TR/html4/strict.dtd'>

<html lang='en'>
  <head>
    <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
    <title>settings</title>

    <!-- Framework CSS -->
    <link rel='stylesheet' href='/css/screen.css' type='text/css' media='screen, projection'>
    <link rel='stylesheet' href='/css/print.css' type='text/css' media='print'>
    <!--[if lt IE]><link rel='stylesheet' href='/css/ie.css' type='text/css' media='screen, projection'><![endif]-->
    <style type='text/css' media='screen'>
      p, table, hr, .box { margin-bottom:25px; }
      .box p { margin-bottom:10px; }
    </style>
  </head>
  <body>
  	<div class='container'>
  		<div class='span-5 append-1'>
  		<ul>
			<li><a href = '/home' class = ''>home</a></li>
			<!--<li><a href = '/converse' class = ''>converse</a></li>-->
			<li><a href = '/favorites' class = ''>favorites</a></li>
		</ul>
		<hr/>		
		<ul>
			<li><a href = '/settings' class = ''>settings</a></li>
			<!--<li><a href = '/log' class = ''>chat log</a></li>-->
			<li><a href = '/signout' class = ''>signout</a></li>
		</ul>
 	</div> 
 		<div>{{realName}}</div>
 		<form action='/settings' method='post' class='span-9'>
 			<div>
 				<h4>Basic information:</h4>
 				<label for='username'>username</label> 
        		<input type='text' name='username'  value='{{username}}' /><br /> 
        		<label for='realName'>real name</label> 
        		<input type='text' name='realName'  value='{{realName}}' /><br /> 
        		<label for='aboutMe'>aboutMe</label> 
        		<input type='text' name='aboutMe'  value='{{aboutMe}}' /> <br />
 			</div>
 			<div>
 				%#setting specific data
 				<br /><h4>tell us more</h4>
 				<label for='location'>location</label> 
        		<input type='text' name='location'  value='{{location}}' /><br /> 
        		<label for='favoriteStuff'>all stuff that interests you: movies, football, etsectra </label> 
        		<input type='text' name='favoriteStuff'  value='{{favoriteStuff}}' /><br /> 
        		<label for='website'>website</label> 
        		<input type='text' name='website'  value='{{website}}' /><br />
 			</div>
 			<div>
 				<h4>friend settings</h4>
 				<ul class='dropdown'>
				%#friends
				%if len(friendList) != 0:
				<li>friends</li>
				%else:
				%pass
				%end
				%for username,friend in friendList.items():
				<li><a href = '/{{username}}' title = '{{friend}}'>{{friend}}</a></li>
				<li><a href = "/setrmf/{{username}}" class = ""> remove </a> 
				</li>
				%end
			</div>
			<input type="submit" class="submitButton small quiet" value="submit &rarr;" />	
		</ul>
 		</form>
 		</div>	
  	<div>
  </body>

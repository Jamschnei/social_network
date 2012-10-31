<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
  <head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>{{realName}}</title>

	<!-- Framework CSS -->
	<script type="text/javascript" src="/css/jquery.js"></script>
	<script src="css/jquery.jgrowl.js"></script>
    <link rel="stylesheet" type="text/css" href="css/jquery.jgrowl.css"/>
	<link rel="stylesheet" href="/css/screen.css" type="text/css" media="screen, projection">
	<link rel="stylesheet" href="/css/print.css" type="text/css" media="print">
	<!--[if lt IE]><link rel="stylesheet" href="/css/ie.css" type="text/css" media="screen, projection"><![endif]-->
	<style type="text/css" media="screen">
      p, table, hr, .box { margin-bottom:25px; }
      .box p { margin-bottom:10px; }
      
      #pop{
      border:1px dashed #333;
      background-color:rgba(0,0,0,0.6);
      padding:20px;
      margin:50px auto;
      position:absolute;
      }
      
	</style>
	<script type="text/javascript">
	$(document).ready(function(){

		//Hide (Collapse) the toggle containers on load
		$("div#addNote").hide();

		//Switch the "Open" and "Close" state per click then slide up/down (depending on open/close state)
		$("a#add").click(function(){
			$(this).toggleClass("active").next().toggle('fast');
			$(this).hide('fast')
		});
		
		$("a#hide").click(function(){
			$('a#add').toggleClass("active").toggle('fast');
			$('div#addNote').hide('fast')
		});	
		
		//Ajax notes send to database
		$('#submit').click(function(){
			$.ajax({
				url : '/addnote',
				type : 'POST',
				data : {'note':$('#note').val(),'email':$('#email').val()},
				
				success:function(returnedValue){
					$('div#addNote').fadeOut('fast');
					$("a#add").fadeIn('fast');
					$.jGrowl(returnedValue,{life:1500});
					$('#note').val("");
					$('#email').val("");
				}
			});
			return false;
			$('#note').val()
		
		});
	});
	</script>
  </head>
  <body>
  	<div class="container">
  		<div class="span-5">
  		<ul>
			%if loggedIn:
				<li><a href = "/home" class = ""> &larr; back home </a></li>
				%if friend:
					<li><a href = "/removefriend" class = ""> &rarr; unfriend </a></li>
				%else:
					%pass
				%end
				
				%if request:
					<li> you request has been sent. </li>
				%end
				%if hasRequested:
					<li>{{realName}} added you as friend 
					<li><a href = "/accept/{{username}}" class = ""> accept </a> | 
					<a href = "/ignore/{{username}}" class = ""> ignore  </a></li>
				%end
				
				%if showAddFriend:
					<li id="addAsFriend"><a href = "/addfriend" class = "" > add as friend </a></li>
				%end
				
				%if owner:
					<li>{{bubbleMessage}}</li>
					<li><a href = "/settings" class = "">settings</a></li>
				%end
				
			%else:
				<li><a href = "/signup" class = ""> join to connect with {{realName}} </a></li>
			%end	
		</ul>
		<hr/>
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
 		</div> 
 		
 		<div class="span-12">
 			<ul>
 			<li>{{realName}} </li>
 			%if aboutMe != '':
 				<li>about : {{aboutMe}} </li>
 			%else:
 				%pass
 			%end
 			%if location != '':
 				<li>location : {{location}} </li>
 			%else:
 				%pass
 			%end
 			%if favoriteStuff != '':
 				<li>favorite stuff : {{favoriteStuff}} </li>
 			%else:
 				%pass
 			%end
 			
 			%if website != '':
 				<li>website : {{website}} </li>
 			%else:
 				%pass
 			%end
 			</ul>
 		</div>	
 		
 		%if addNote:	
			<a href = "javascript:" id="add">add a note</a>
 			<div class="span-12" id="addNote">
 				<a href="javascript:" id="hide">close this box</a>
				<form action="/addnote" method="post" name="addNote">
 					<label for="note">Note</label>
 					<input type="text" name="note" id="note"><br/>
 					%if loggedIn == False:
 						<label for="email">email</label>
 						<input type="text" name="email" id="email"><br/>
 					%end
 					<input type="submit" id="submit">
				</form>
 			</div>
		%end
		
  </body>

<!doctype html>
<html>
<head>
<style type="text/css">
html{
	background-color:#50a443;
	text-align:center;
	}
	
form span {
	padding:4px;
	margin:8px;
	}
	
input{
	padding:4px;
	text-transform:lowercase;
	}
	
#signin{
	width:600px;
}
</style>
	
</head>


	<div id="bubble">{{bubbleMessage}}</div>
	
	<div id="signin">
	<form action='/signin' method='post'>
		<span>username or email :</span><input type="text" name="user" required/><br/>
		<span>password :</span><input type="password" name="password" required/><br/>
		<input type="submit" value="Ok"/>		
	</form>	
	</div>
</html>

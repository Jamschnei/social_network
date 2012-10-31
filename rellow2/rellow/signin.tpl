<!DOCTYPE html>
<html>
<head>
<style type="text/css">
ul
{
	list-style:none;
} 
body 
{
	font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
	padding: 100px;
	background-image:url(/css/tile.jpg);
}

.main
{
	position:relative;
	margin: 0 auto;
	padding:30px 10px;
	border:1px dashed #ADADAD;
	width:500px;
	height:150px;
 	-webkit-border-radius: 3px;
 	-moz-border-radius: 3px;
 	border-radius: 3px;
}

.floatLeft{
	position:absolute;
	float:left;
	margin-left:70px;
	margin-top:3px;
}

.floatRight{
	float:right;
	text-align:right;
	margin-right:400px;
}

.floatRight li
{
	padding:4px 0;
}

.simpleInput{
	background-color:#fff;
	padding:5px;
	border:1px solid #DAE2E9;
 	-webkit-border-radius: 3px;
 	-moz-border-radius: 3px;
 	border-radius: 3px;
}

.simpleInput:focus{
	background-color:#f8f8f8;
}

.small
{
	font-size: .8em; margin-bottom: 1.875em; line-height: 1.875em; 
}

.large
{
	font-size: 1.2em; line-height: 2.5em; margin-bottom: 1.25em; 
}

.quiet
{ 
	color: #666; 
}

.loud
{ 
	color: #000; 
}

.highlight  
{ 
	background:#ff0; 
}

.submitButton
{
	text-transform:lowercase;
	padding:4px 6px;
	margin:-80px 70px 0 0;
	float:right;
}

</style>
<title>signin</title>
</head>
<body>
	<div class="main">
		<form class = "small quiet" action="/signin" method="post">
			<div class="floatRight">
				<ul>
					<li>username </li>
					<li>password </li>
				</ul>	
			</div>
			<div class = "floatLeft">
				<ul>
					<li><input type="text" name="user" class="simpleInput quiet" /></li>
					<li><input type="password" name="password" class="simpleInput quiet" /></li>				
				</ul>
			</div>
			<input type="submit" class="submitButton small quiet" value="submit &rarr;" />
		</form>
	</div>
	<div class="loud">{{bubbleMessage}}</div>
</body>
</html>

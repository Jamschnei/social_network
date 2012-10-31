<!doctype html>
<html>
<head>
<style type="text/css">
*
{
	margin:0;
	padding:0;
	font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}
ul
{
	list-style:none;
} 
form span 
{
	padding:4px;
	margin:8px;
}
	
input
{
	padding:4px;
	text-transform:lowercase;
}
	
#sidebar
{
	background: #fff url(http://dl.dropbox.com/u/5230551/bg.png);
	float:left;
	padding:10px 0 50% 30px;
	width:200px;
	height:100%;
	border-right:1px  solid #333;
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

</head>
<body>
<div id = "sidebar">
	<ul>
		%#friends
		%for frnd in f:
		<li><a href = '/{{frnd}}' title = "{{frnd}}">{{f}}</a></li>
		%end
	</ul>
	<ul>
		<li><a href = "/home" class = "quiet small">home</a></li>
		<li><a href = "/converse" class = "quiet small">converse</a></li>
		<li><a href = "/favorites" class = "quiet small">favorites</a></li>
	</ul>
	<hr/>
	<ul>
		%#friend requests
		%for req in fr: 
		<li><a href="/{{req}}" title = "friend request from {{req}}" class = "quiet small">{{req}}</a> -- <a href="/accept/{{req}}">accept</a> |
		<a href="/ignore/{{req}}" class = "quiet small">ignore</a></li>
		%end
	</ul>
	<ul>
		<li><a href = "/settings" class = "quiet small">settings</a></li>
		<li><a href = "/log" class = "quiet small">chat log</a></li>
		<li><a href = "/signout" class = "quiet small">signout</a></li>
	</ul>
	
</div>
<div id = "content" class = "quiet small">
Hi dear <strong class = "quiet small">{{realName}}</strong> : {{aboutMe}}
</div>

</body>

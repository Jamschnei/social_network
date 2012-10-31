<!doctype html>
<html>
<head>
<style type="text/css">
html{
	background-color:#50a443;
	margin:5px auto;
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

#sidebar{
	float:left;
	margin: 10px 0 0 10px;
	width:200px;

}
</style>
	
</head>
<body>
<div id = "sidebar">
%for row in rows:
	%friends = row[2].split()
	%for f in friends:
	<ul>
		<li>{{f}}</li>
	</ul>
	%end
	
	%photos = row[3].split()
	%for p in photos:
	<ul>
		<li>{{p}}</li>
	</ul>
	%end 
%end
</div>
<div id = "content">
</div>

</body>

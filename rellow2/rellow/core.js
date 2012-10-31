function ajaxSend(url,data,containerId)
{
		$.ajax({
		url     : url,
		type    : "POST",
		data    : data,
		success : function(returndeValue){
			$('#'+containerId).text(returndeValue);
		}		
	});
	//*/
}

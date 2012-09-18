/*
* DCU Web interface
*  Alexandr Krupenkin
*/

$(document).ready(function(){
	$("#login-dialog").dialog({
		autoOpen: true,
		height: 190,
		width: 260,
		modal: true,
		resizable: false,
		buttons: {
			"Ok" : function(){
				try_auth($("#name").val(), $("#password").val());
			}
		},
		close: function(event, ui){
			$(this).dialog("open");
		}
	});
});

function try_auth(name, password){
	$.ajax({
		type: "GET",
		dataType: "json",
		url: "ajax/",
		data: { 
			"server": "login", 
			"name": name, 
			"password": password },
		success: function(data) {
			if (data["auth"] == true){
				$("#username").text(data["name"]);
				$("#login-dialog").dialog("destroy");
			}
			else {
				$("#login").addClass("ui-state-error");
				$("#password").addClass("ui-state-error");
			}
		}
	});
}

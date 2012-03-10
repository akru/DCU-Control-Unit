/*
* DCU Web interface
*  Alexandr Krupenkin
*/

$(document).ready(function() {
	$( "#client-select-button" ).button({
		text: false,
		icons: {
			primary: "ui-icon-plus"
		}
	}).click(function() {
		$.ajax({
			type: "GET",
			dataType: "json",
			url: "ajax/",
			data: { "server": "clist" },
			success: function(data) {
				create_select_dialog(data["html"]);
			}
		});
	});
	$( "#logout-button" ).button({
		text: false,
		icons: {
			primary: "ui-icon-close"
		}
	}).click(function() {
		$.ajax({
			type: "GET",
			dataType: "json",
			url: "ajax/",
			data: { "server": "logout" },
			success: function(data) {
				if (data["logout"])
					location.reload(true);
			}
		});
	});
});

function create_select_dialog(client_list) {
	$("body").append(client_list);
	$("#client-list").selectable();
	$("#client-select-dialog").dialog({
		autoOpen: true,
		show: "fade",
		hide: "fade",
		height: 300,
		width: 350,
		minHeight: 300,
		minWidth: 350,
		modal: true,
		buttons: {
			Ok: function() {
				$.each($("#client-list li.ui-selected"),
					function(index, val) {
						create_client_window($($(val).children()[0]).text(), 
							$($(val).children()[1]).text());
				});
				$(this).dialog("close");
				$(this).dialog("destroy");
			}
		}
	});
}

function create_client_window(name, module_name) {
	var windowId = "#client-window-" + name;
	if ($(windowId).length > 0)
		return;
	$.ajax({
		type: "GET",
		dataType: "json",
		url: "ajax/",
		data: { "server": "cview", "module_name": module_name},
		success: function(ui) {
			// Append window block
			$("body").append(
				"<div id=\"client-window-" + name + 
				"\" style=\"display:none\">" + ui["html"] + "</div>"
			);
			// Create window
			$(windowId).dialog({
				autoOpen: true,
				show: "fade",
				hide: "fade",
				title: module_name + " :: " + name,
				buttons: { 
					"activate" : function(){ start_stop_control(true, name) },
					"deactivate": function(){ start_stop_control(false, name) }
				},
				close: function() {
					$(this).dialog("destroy");
					$(this).remove(); 
				}
			});
		}
	});
}

function start_stop_control(is_begin, client_name) {
  var cmd = "cstop"
  if (is_begin) cmd = "cstart";
	$.ajax({
		type: "GET",
		dataType: "json",
		url: "ajax/",
		data: { "server": cmd, "name": client_name},
		success: function(result){
			if (result["server"] == "OK") {
				$("#client-window-" + name).addClass("active");
			}
			else {
			  $("#client-window-" + name)
					.html("<h3>Error activate control:</h3>" + result["server"])
			}
		}
	});
}

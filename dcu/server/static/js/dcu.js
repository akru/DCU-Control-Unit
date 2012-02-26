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
			url: "ajax",
			data: { "server": "clist" },
			success: function(data) {
				create_select_dialog(data);
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
			url: "ajax",
			data: { "server": "logout" },
			success: function(data) {
				if (data["logout"])
					location.reload(true);
			}
		});
	});
});

function create_select_dialog(client_list) {
	$("#client-list").html("");
	for (i in client_list) {
		$("#client-list")
			.append(
				"<li class=\"ui-widget-content\" index=\"" + i + "\">" + 
				"<div class=\"client-name\">" + 
				client_list[i]["name"] + 
				"</div><div class=\"client-class\">" + 
				client_list[i]["class"] + 
				"</div></li>");
	}
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
						create_client_window(client_list[$(val).attr("index")]);
				});
				$(this).dialog("close");
			}
		}
	});
}

function create_client_window(client) {
	var windowId = "#client-window-" + client["name"];
	if ($(windowId).length > 0)
		return;
	$.ajax({
		type: "GET",
		dataType: "json",
		url: "ajax",
		data: { "req": "client_ui", "class": client["class"] },
		success: function(ui) {
			// Append window block
			$("body").append(
				"<div id=\"client-window-" + client["name"] + 
				"\" style=\"display:none\">" + ui["html"] + "</div>"
			);
			// Create button list
			var buttonsList = {};
			$.each(ui["buttons"], function(name, cmd) {
				buttonsList[name] = 
					function() { ajax_send_cmd(cmd, client); };
			});
			// Create window
			$(windowId).dialog({
				autoOpen: true,
				show: "fade",
				hide: "fade",
				title: client["class"] + " :: " + client["name"],
				height: ui["height"],
				width: ui["width"],
				minHeight: ui["height"],
				minWidth: ui["width"],
				buttons: buttonsList,
				close: function() {
					$(this).stopTime();
					$(this).dialog("destroy");
					$(this).remove(); 
				}
			});
			// Starting update state timer
			$(windowId).everyTime(1000, 
					function(){
						$.ajax({
							type: "GET",
							dataType: "json",
							url: "ajax",
							data: {
								"req" : "stream_json",
								"class" : client["class"],
								"name" : client["name"]
							},
							success: function(data) {	
								$.each(data, function(row, row_value) {
									if (row_value["html"]) {
										$(windowId + " ." + row).html(row_value["html"]);
									}
									if (row_value["attr"]) {
										$.each(row_value["attr"], function(attr, attr_value) {
											$(windowId + " ." + row).attr(attr, attr_value);
										});
									}
								});
							}
						});
				});
		}
	});
}

function ajax_send_cmd(client_cmd, client) {
	$.ajax({
		type: "GET",
		dataType: "json",
		url: "ajax",
		data: { 
			"req" : "client_cmd",
			"class" : client["class"],
			"name" : client["name"],
			"cmd" : client_cmd
		}
	});
}


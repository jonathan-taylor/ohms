/*
 *  This Source Code Form is subject to the terms of the Mozilla Public
 *  License, v. 2.0. If a copy of the MPL was not distributed with this
 *  file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 *  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>
 */

$(document).ready(function() {
    $.ajax({
	url : ROUTE_FILE,
	type : "GET",
	dataType : "json",
	success : function(data) {

	    var now = new Date();
	    $(".loading").remove();
	    
	    var homeworks = data["hw_list"];
	    for(var i=0; i<homeworks.length; i++) {
		var hw = homeworks[i];
		row = $("<tr />");
		row.append("<td><a href='view.html?id="+hw.id+"'>"+hw.name+"</a></td>");
		row.append("<td>"+hw.due_date+"</td>");

		var due_date = new Date(hw.due_date);
		if (now.getTime() > due_date.getTime()) {
		    row.append("<td><a href='sols.html?id="+hw.id+"'>Solutions</a></td>");
		} else {
		    row.append("<td></td>");
		}
		$("#homeworks").children("tbody").append(row);
	    }
	},
	error: function(jqXHR,textStatus,errorThrown) {
	    if(textStatus.status==401) {
		alert("Error: You may have been logged out. Please refresh the page and try again.");
	    } else {
		alert("Internal Server Error: Please contact a system administrator.");
		console.log(jqXHR);
	    }
	},
    });
});
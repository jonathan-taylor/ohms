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

	    $(".loading").remove();

	    $("#studentName").html("You are logged in as <strong>" +
				   data["student_name"] + "</strong>.");

	    var grades = data.grades;
 	    var table_body = $("#grades").find("tbody");
	    if(grades.length===0) {
		table_body.append("<tr><td>No records found.</td></tr>");
	    } else {
		for(var i=0; i<grades.length; i++) {
		    table_body.append("<tr><td>" + grades[i].homework + "</td>"+
				      "<td>" + grades[i].score + "</td>" + 
				      "<td>" + grades[i].max + "</td></tr>"); 
		}
	    }
	},
	error: function(jqXHR,textStatus,errorThrown) {
	    if(jqXHR.status==401) {
		alert("Error: You may have been logged out. Please refresh the page and try again.");
	    } else if(jqXHR.status==403) {
		alert("Error: No gradebook was found. Has it been set up?");
	    } else {
		alert("Internal Server Error: Please contact a system administrator.");
	    }
	},
    });
});

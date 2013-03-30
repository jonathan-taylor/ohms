/*
 *  This Source Code Form is subject to the terms of the Mozilla Public
 *  License, v. 2.0. If a copy of the MPL was not distributed with this
 *  file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 *  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>
 */

var OHMS = (function(OHMS) {

    var FileUploadAnswer = function(question, data) {
	this.text = data.text;
	this.max_pts = data.max_pts;
	this.solution = data.solution;
	OHMS.Answer.apply(this, arguments);
    }

    FileUploadAnswer.prototype = new OHMS.Answer();

/*
    FileUploadAnswer.prototype.bind_events = function () {
	var that = this;
	var q = this.question;
	q.element.find(".submit").click(function () {
	    var data = new FormData();
	    data.append("action","upload_file");
	    data.append("q_id",q.get_question_id());
	    data.append("file",that.get_file.files[0]);
	    var req = new XMLHttpRequest();
	    req.open("POST",ROUTE_FILE,true);
	    req.onload = function(event) {
		console.log(event);
		if(req.status === 200)
		    that.element.find(".msg").text("File uploaded!");
		else
		    that.element.find(".msg").text("Error in uploading file.");
	    }
	    req.send(data);
	})
    }
*/

    FileUploadAnswer.prototype.get_file = function () {
	return this.element.get(0);
    }

    FileUploadAnswer.prototype.create_element = function () {
/*	this.element = $("<div class='Answer'/>");
	this.element.append("<input type='file' class='file'/>");
*/
	this.element = $("<input type='file' class='Answer'/>");
    }

    FileUploadAnswer.prototype.show_solution = function () {
	this.element = null;
    }

    FileUploadAnswer.prototype.set_value = function () {
    }

    FileUploadAnswer.prototype.get_value = function () {
	return this.get_file().files[0]
    }

    OHMS.FileUploadAnswer = FileUploadAnswer;

    return OHMS;

}(OHMS))
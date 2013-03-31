/*
 *  This Source Code Form is subject to the terms of the Mozilla Public
 *  License, v. 2.0. If a copy of the MPL was not distributed with this
 *  file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 *  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>
 */

var OHMS = (function(OHMS) {

    var Question = function () {
	this.element = null;
	this.homework = null;
	this.answers = null;
	// keep track of last 2 submission times
	this.last_times = null;
	// metadata for question
	this.question_name = null;
	this.question_id = null;
	this.question_comments = null;
	this.body = null;
	this.comments = null;
    }

    Question.prototype.create_element = function () {
	var name = $("<h3 class='questionName'/>");

	var row1 = "<tr> \
<td class='span7'><div class='score'></div></td> \
<td class='span3'><b>Comments</b></td>           \
</tr>";
	var row2 = "<tr>   \
<td class='body'></td>     \
<td class='comments'></td> \
</tr>";
	var frame = $("<table class='frame'/>").html(row1 + row2);
	
	var submit = $("      \
<button class='submit' disabled>Submit Response</button> \
<span class='time'></span>");

	var question = $("<div class='question'/>").append(name).append(frame).append(submit);
	$("#homework").append(question).append("<hr>");

	this.element = question;
	this.element.data("question",this);
	this.bind_events();
    }

    Question.prototype.bind_events = function () {
	var that = this;
	// submit onclick handler
	this.element.find(".submit").click(function () {
	    that.submit_response();
	})
    }

    Question.prototype.get_question_name = function () {
	return this.question_name;
    }

    Question.prototype.set_question_name = function(name) {
	this.question_name = name;
	this.element.children(".questionName").text(name)
    }

    Question.prototype.get_question_id = function () {
	return this.question_id;
    }

    Question.prototype.set_question_id = function(id) {
	this.question_id = id;
	this.element.attr("id",id);
    }

    Question.prototype.get_body = function () {
	return this.body;
    }

    Question.prototype.set_body = function (data, context) {
	if (data.parts !== undefined) {
	    context.append("<p>" + data.text + "</p>");
	    var parts = $("<ol class='ohms-ol'/>").appendTo(context);
	    for (var i=0; i<data.parts.length; i++) {
		var part = $("<li/>").appendTo(parts);
		this.set_body(data.parts[i],part);
	    }
	    return false;
	} else if (data.type === "FillInTheBlank") {
	    // generate HTML string
	    var string = "";
	    var blanks = [];
	    var max_pts = 0;
	    for (var i=0; i<data.body.length; i++) {
		if (data.body[i].type === undefined) {
		    string += data.body[i];
		} else {
		    string += "<input type='text' disabled></input>";
		    blanks.push(i);
		    max_pts += parseFloat(data.max_pts);
		}
	    }
	    // add HTML to the DOM
	    context.append("<p><strong>[" + max_pts + 
			   " pts]</strong> " + string + "</p>");
	    // instantiate answer object alongside the DOM object
	    var elements = context.find("input");
	    for (var j=0; j<elements.size(); j++) {
		if (data.solution !== undefined) {
		    new OHMS.FillInTheBlankAnswer(this,elements.eq(j),
						  data.body[blanks[j]],
						  data.solution.answer[j]);
		} else {
		    new OHMS.FillInTheBlankAnswer(this,elements.eq(j),
						  data.body[blanks[j]]);
		}
	    }
	} else {
	    context.append("<p><strong>[" + data.max_pts + 
			   " pts]</strong> " + data.text + "</p>");
	    if (data.type === "MultipleChoice") {
		var answer = new OHMS.MultipleChoiceAnswer(this,data);
		context.append(answer.element);
	    } else if (data.type === "MultipleResponse") {
		var answer = new OHMS.MultipleResponseAnswer(this,data);
		context.append(answer.element);
	    } else if (data.type === "TrueFalse") {
		var answer = new OHMS.TrueFalseAnswer(this,data);
		context.append(answer.element);
	    } else if (data.type === "ShortAnswer") {
		var answer = new OHMS.ShortAnswer(this,data);
		context.append(answer.element);
	    } else if (data.type === "FileUpload") {
		var answer = new OHMS.FileUploadAnswer(this,data);
		context.append(answer.element);
	    } else if (data.type === "LaTeXAnswer") {
		var answer = new OHMS.LaTeXAnswer(this,data);
		context.append(answer.element);
	    } else {
		context.append(data.text);
	    }
	}
	if (data.solution !== undefined)
	    context.append("<p class='solution'>"+data.solution.text+"</p>");
    }

    Question.prototype.get_comments = function () {
	return this.comments;
    }

    Question.prototype.set_comments = function (comments) {
	this.comments = comments;
	var comments_list = $("<ul/>");
	for(var i=0; i<comments.length; i++) {
	    if(comments[i])
		comments_list.append("<li>" + comments[i].replace(/\n/g,'<br />') + "</li>");
	}
	this.element.find(".comments").empty().append(comments_list);
    }

    Question.prototype.set_score = function (points) {
	if (points.earned == points.total) {
	    var score_string = "Congrats! You've earned all \
<font color=green>" + points.total + "</font> points for this question.";
	} else {
	    points.missed = points.graded - points.earned;
	    points.ungraded = points.total - points.graded;
	    var score_string = "Score: <font color=green>" + points.earned +
		"</font> correct";
	    if(points.missed) 
		score_string += ", <font color=red>" + points.missed + "</font> incorrect";
	    if(points.ungraded)
		score_string += ", <font color=gray>" + points.ungraded + "</font> ungraded";
	    score_string += " [out of " + points.total + " possible points]";
	}
	this.element.find(".score").html(score_string);
    }

    Question.prototype.set_time = function (last_times) {
	this.last_times = last_times;
	var n = this.last_times.length;
	if (n === 1) {
	    this.element.find(".time").html("(<strong>Last submission:</strong> "+last_times[0]+")");
	} else if(n > 1) {
	    this.element.find(".time").html("(<strong>Last submissions:</strong> "+last_times[n-2]+" and "+last_time[n-1]+ ")");
	}
    }

    Question.prototype.get_homework = function () {
	return this.homework;
    }

    Question.prototype.set_homework = function () {
	homework = this.element.parent("#homework");
	this.homework = homework.data("homework");
    }


    Question.prototype.load_response = function () {
	$.ajax({
	    url : ROUTE_FILE,
	    type : "POST",
	    data : {
		action : "load_response",
		q_id: this.element.attr("id"),
	    },
	    dataType : "json",
	    success : $.proxy(this.load_response_success,this),
	    error : this.load_response_error,
	});
    }

    Question.prototype.load_response_error = function (jqXHR, textStatus,
    errorThrow) {
	if (jqXHR.status == 403) {
	    alert("Error: It appears that the homework is not tied to a \
database. The admin should set up a database or update the database IDs.");
	} else {
	    alert("There was an error loading your previous response to a question.");
	}
    }

    Question.prototype.load_response_success = function (data) {

	var now = new Date(data.current_time);

	// fetch all the answer elements
	this.answers = this.element.find(".Answer");

	// if no response has been submitted
	if(data.last_times === undefined) {
	    // unlock questions if due date has not passed
	    if(now.getTime() <= this.homework.due_date.getTime())
		this.unlock_question();
	    // exit function
	    return false;
	}

	// iterate over form elements, populating their value
	for(var i=0; i<this.answers.size(); i++) {
	    // get answer element and value
	    var answer = data.answers[i]
	    // set values (separate cases for buttons and multiple choice)
	    this.answers.eq(i).data("answer").set_value(answer);
	}

	// show score at top of question
	this.set_score(data.points);
	// show comments
	this.set_comments(data.comments);
	// print the timestamps of last two submissions
	this.set_time(data.last_times);
	// unlock the question if user can resubmit
	if (!data.locked) {
	    this.unlock_question();
	}
    }

    Question.prototype.lock_question = function () {
	for (var i=0; i<this.answers.size(); i++) {
	    this.answers.eq(i).data("answer").lock_answer();
	}
	this.element.find(".submit").attr("disabled","disabled");
    }

    Question.prototype.unlock_question = function () {
	for (var i=0; i<this.answers.size(); i++) {
	    this.answers.eq(i).data("answer").unlock_answer();
	}
	this.element.find(".submit").removeAttr('disabled');
    }

    Question.prototype.submit_response = function () {
	this.lock_question();
	var answers = this.answers;
	var that = this;
	var data = new FormData();
	data.append("action","submit_response");
	data.append("q_id",this.element.attr("id"));
	for (var i=0; i<answers.size(); i++) {
	    data.append("answers",answers.eq(i).data("answer").get_value());
	}
	var req = new XMLHttpRequest();
	req.open("POST",ROUTE_FILE,true);
	req.onload = function (event) {
	    if(event.target.status === 200) {
		data = JSON.parse(event.target.response);
		$.proxy(that.submit_response_success,that)(data);
	    } else {
		that.submit_response_error(event.target.status);
	    }
	}
	req.onerror = this.submit_response_error;
	req.send(data);
    }

    Question.prototype.submit_response_success = function (data) {
	this.set_time(data.last_times);
	this.set_score(data.points);
	this.set_comments(data.comments);
	if (!data.locked) {
	    this.unlock_question();
	}
    }

    Question.prototype.submit_response_error = function (status) {
	if (status === 400) {
	    alert("There was an error recording your response. The \
response was not in the expected format. Perhaps you entered a non-number \
where a number was expected?");
	    this.unlock_question();
	} else if (status === 401) {
	    alert("There was an error recording your response. You \
may have been logged out? Save your work and try refreshing the page.");
	} else if (status === 410) {
	    alert("There was an error recording your response. The \
deadline has passed.");
	} else if (status === 423) {
	    alert("There was an error recording your response. You \
have made too many submissions.");
	} else {
	    alert("There was an error submitting your response. Please \
try again.");
	    this.unlock_question();
	}
	
    }

    OHMS.Question = Question;

    return OHMS;

}(OHMS))

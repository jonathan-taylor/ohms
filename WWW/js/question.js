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
	this.last_time = null;
	this.last_last_time = null;
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
	    } else if (data.type === "TrueFalse") {
		var answer = new OHMS.TrueFalseAnswer(this,data);
		context.append(answer.element);
	    } else if (data.type === "ShortAnswer") {
		var answer = new OHMS.ShortAnswer(this,data);
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
		comments_list.append("<li>" + comments[i] + "</li>");
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

    Question.prototype.set_time = function (last_time, last_last_time) {
	this.last_time = last_time;
	if (last_last_time === null) {
	    this.element.find(".time").html("(<strong>Last submission:</strong> "+last_time+")");
	} else {
	    this.last_last_time = last_last_time;
	    this.element.find(".time").html("(<strong>Last submissions:</strong> "+last_last_time+" and "+last_time+ ")");
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

    Question.prototype.load_response_error = function (xhr, textStatus,
    errorThrow) {
	console.log(xhr.responseText);
    }

    Question.prototype.load_response_success = function (data) {

	var now = new Date();

	// if no response has been submitted
	if(data==null) {
	    // unlock questions if due date has not passed
	    if(now.getTime() <= this.homework.due_date.getTime())
		this.unlock_question();
	    // exit function
	    return false;
	}

	// fetch all the answer elements
	this.answers = this.element.find(".Answer");

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
	this.set_time(data.last_time, data.last_last_time);
	// unlock the question if user can resubmit
	this.unlock_question_if_possible();
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

    // this unlocks a question only if it's been 6 hours since the 
    // next-to-last submission and homework deadline hasn't passed
    Question.prototype.unlock_question_if_possible = function () {
	var now = new Date();
	var lastLastTime = new Date(this.last_last_time);
	var h = 6;
	if (now.getTime() > lastLastTime.getTime()+(h*3600000) &&
	    now.getTime() <= this.homework.due_date.getTime())
            this.unlock_question();
    }

    Question.prototype.submit_response = function () {
	this.lock_question();
	var answers = []
	for (var i=0; i<this.answers.size(); i++) {
	    answers[i] = this.answers.eq(i).data("answer").get_value();
	}
	$.ajax({
	    url : ROUTE_FILE,
	    type : "POST",
	    data : {
		action : "submit_response",
		q_id : this.element.attr("id"),
		answers : JSON.stringify(answers)
	    },
	    dataType : "json",
	    success : $.proxy(this.submit_response_success,this),
	    error : this.submit_response_error,
	});
    }

    Question.prototype.submit_response_success = function (data) {
	this.set_time(data.last_time, data.last_last_time);
	this.set_score(data.points);
	this.set_comments(data.comments);
	this.unlock_question_if_possible();
    }

    Question.prototype.submit_response_error = function (xhr) {
	console.log(xhr.responseText);
    }

    OHMS.Question = Question;

    return OHMS;

}(OHMS))
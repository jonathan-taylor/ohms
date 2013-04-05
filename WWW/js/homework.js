/*
 *  This Source Code Form is subject to the terms of the Mozilla Public
 *  License, v. 2.0. If a copy of the MPL was not distributed with this
 *  file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 *  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>
 */

var OHMS = (function(OHMS) {

    var Homework = function () {
	this.element = $("#homework");
	this.element.data("homework",this);
	this.homework_name = null;
	this.due_date = null;

	MathJax.Hub.Config({
	    tex2jax: {
		inlineMath: [['$','$'], ['\\(','\\)']],
		processEscapes: true,
		skipTags: ["script","noscript","style","textarea","code"]
	    }
	});

    }

    Homework.prototype.get_homework_name = function () {
	return this.homework_name;
    }

    Homework.prototype.set_homework_name = function (name) {
	this.homework_name = name;
	this.element.children("#homework_name").text(name);
    }

    Homework.prototype.get_homework_text = function () {
	return this.homework_text;
    }

    Homework.prototype.set_homework_text = function (text) {
	this.homework_text = text;
	this.element.children("#homework_text").html(text);
    }

    Homework.prototype.get_due_date = function () {
	return this.due_date;
    }

    Homework.prototype.set_due_date = function (date_string) {
	this.due_date = new Date(date_string);
    }

    Homework.prototype.load_homework = function () {
	$.ajax({
	    url : ROUTE_FILE,
	    type : "POST",
	    data : { action : "load_homework" },
	    dataType : "json",
	    success : $.proxy(this.load_homework_success,this),
	    error: $.proxy(this.load_homework_error,this),
	});
    }

    Homework.prototype.load_homework_error =
    function(jqXHR,textStatus,errorThrow) {
	if(jqXHR.status==404) {
	    alert("Error: The homework you requested was not found.");
	} else if (jqXHR.readyState) {
	    alert("There was an error loading the homework \
you requested. Try refreshing the page.");
	}
    }

    Homework.prototype.load_homework_success = function(data) {

	// set student name
	$("#studentName").html("You are logged in as <strong>" +
			       data["student_name"] + "</strong>.");

	// set metadata associated with homework
	this.set_homework_name(data["name"]);
	this.set_homework_text(data["text"]);
	this.set_due_date(data["due_date"]);

	// get elements
	var questions = data["questions"];

	// iterate over questions
	for(var i=0; i<questions.length; i++) {

	    var q = questions[i];

	    // initialize empty question object
	    var question = new OHMS.Question();
	    question.create_element();

	    // set basic properties
	    question.set_question_id("q"+i);
	    question.set_homework();
	    
	    // question title
	    title = "Question " + (i+1);
	    if(q.name) title += ": " + q.name;
	    question.set_question_name(title);

	    // question body
	    var body = question.element.find(".body");
	    question.set_body(q.data, body);

	    // load student response if data does not include solutions
	    if(q.data.solution===undefined)
		question.load_response();

	    // otherwise, remove comments section
	    else
		question.element.find(".frame").replaceWith(body.html());

	}

	MathJax.Hub.Typeset();

	$(".loading").remove();
	
    }

    OHMS.Homework = Homework;

    return OHMS;

}(OHMS))
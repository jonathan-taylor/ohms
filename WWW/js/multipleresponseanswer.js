/*
 *  This Source Code Form is subject to the terms of the Mozilla Public
 *  License, v. 2.0. If a copy of the MPL was not distributed with this
 *  file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 *  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>
 */

var OHMS = (function(OHMS) {

    var MultipleResponseAnswer = function(question, data) {
	this.text = data.text;
	this.choices = data.choices;
	this.compact = data.compact;
	this.solution = data.solution;
	this.max_pts = data.max_pts;
	this.id = Math.random().toString(36).substring(7);
	OHMS.Answer.apply(this, arguments);
    }

    MultipleResponseAnswer.prototype = new OHMS.Answer();

    MultipleResponseAnswer.prototype.create_element = function () {

	this.element = $("<div class='Answer MultipleResponse' />");

	if (this.compact) {
	    for (var i=0; i<this.choices.length; i++) {
		this.element.append("<input type='checkbox' name='"+this.id+"' value="+i+" disabled> " + this.choices[i] + "&nbsp;&nbsp;&nbsp;");
	    }
	} else {
	    for (var i=0; i<this.choices.length; i++) {
		this.element.append("<p><input type='checkbox' name='"+this.id+"' value="+i+" disabled> " + this.choices[i] + "</p>");
	    }
	}
    }

    MultipleResponseAnswer.prototype.show_solution = function () {
        var answers = this.solution.answer.split(",");
        for (var i=0; i<this.choices.length; i++) {
	    this.element.find("input[value="+answers[i]+"]").attr("checked","checked");
        }
    }

    MultipleResponseAnswer.prototype.get_element_by_value = function (value) {
	return this.element.find("[value="+value+"]");
    }

    MultipleChoiceAnswer.prototype.get_value = function () {
	return this.element.find(":checked").val();
    }

    MultipleChoiceAnswer.prototype.set_value = function (value) {
	this.get_element_by_value(value).attr("checked","checked");
    }

    MultipleChoiceAnswer.prototype.unlock_answer = function () {
	this.element.find("input").removeAttr("disabled");
    }

    MultipleChoiceAnswer.prototype.lock_answer = function () {
	this.element.find("input").attr("disabled","disabled");
    }


    OHMS.MultipleChoiceAnswer = MultipleChoiceAnswer;

    return OHMS;

}(OHMS))

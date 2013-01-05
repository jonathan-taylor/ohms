/*
 *  This Source Code Form is subject to the terms of the Mozilla Public
 *  License, v. 2.0. If a copy of the MPL was not distributed with this
 *  file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 *  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>
 */

var OHMS = (function(OHMS) {

    var TrueFalseAnswer = function(question, data) {
	this.text = data.text;
	this.max_pts = data.max_pts;
	this.solution = data.solution;
	OHMS.Answer.apply(this, arguments);
    }

    TrueFalseAnswer.prototype = new OHMS.Answer();

    TrueFalseAnswer.prototype.create_element = function () {

	this.element = $("<div class='Answer TrueFalse btn-group' \
data-switch='true' data-toggle='buttons-radio'/>");

	this.element.html("\
  <button type='button' class='btn btn-mini' value='t' disabled> \
      True</button>                                                     \
  <button type='button' class='btn btn-mini' value='f' disabled> \
      False</button>");

    }

    TrueFalseAnswer.prototype.bind_events = function () {
	this.element.on("click", ".btn", function() {
	    var $this = $(this);
	    if (!$this.hasClass("btn-info")) {
		$this.addClass("btn-info");
		$this.siblings().removeClass("btn-info");
	    }
	});
    }

    TrueFalseAnswer.prototype.show_solution = function () {
	this.get_element_by_value(this.solution.answer).addClass("btn-info");
    }

    TrueFalseAnswer.prototype.get_element_by_value = function (value) {
	return this.element.find("[value="+value+"]");
    }

    TrueFalseAnswer.prototype.get_value = function () {
	return this.element.children(".btn-info").val();
    }

    TrueFalseAnswer.prototype.set_value = function (value) {
	this.get_element_by_value(value).addClass("btn-info");
    }

    TrueFalseAnswer.prototype.unlock_answer = function () {
	this.element.children("button").removeAttr("disabled");
    }

    TrueFalseAnswer.prototype.lock_answer = function () {
	this.element.children("button").attr("disabled","disabled");
    }


    OHMS.TrueFalseAnswer = TrueFalseAnswer;

    return OHMS;

}(OHMS))
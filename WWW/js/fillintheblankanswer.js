/*
 *  This Source Code Form is subject to the terms of the Mozilla Public
 *  License, v. 2.0. If a copy of the MPL was not distributed with this
 *  file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 *  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>
 */

var OHMS = (function(OHMS) {

    var FillInTheBlankAnswer = function(question,jQueryElt,data,solution) {
	this.element = jQueryElt;
	this.type = data.type;
	this.solution = solution;
	this.max_pts = data.max_pts;
	OHMS.Answer.apply(this, arguments);
    }

    FillInTheBlankAnswer.prototype = new OHMS.Answer();

    FillInTheBlankAnswer.prototype.create_element = function () {

	if (this.type === "Float") {
	    this.element.addClass("Answer input-small");
	} else {
	    this.element.addClass("Answer input-large");
	}

    }

    FillInTheBlankAnswer.prototype.show_solution = function () {

	// helper function that casts answers into appropriate form
	cast_answer = function(answer) {
	    // take average of answers that were specified as ranges
	    if (answer instanceof Array && typeof answer[0]=="number")
		answer = 0.5*(answer[0]+answer[1]);
	    // round answers (to handle floating point precision)
	    if (typeof answer === "number") {
		if (Math.round(answer) == answer)
		    return answer;
		else if (Math.abs(answer) > 10)
		    return answer.toFixed(1);
		else
		    return answer.toPrecision(2);
	    }
	    return answer;
	}

	// if there were multiple possible answers
	if (this.solution instanceof Array) {
	    // iterate over the answers
	    for (var i=0; i<this.solution.length; i++)
		this.solution[i] = cast_answer(this.solution[i]);
	    // separate possible answers by "or"
	    this.solution = this.solution.join(" or ");
	} else {
	    this.solution = cast_answer(this.solution);
	}
	this.element.replaceWith("<span class='solution'><u>"+this.solution+"</u></span>");

    }

    OHMS.FillInTheBlankAnswer = FillInTheBlankAnswer;

    return OHMS;

}(OHMS))
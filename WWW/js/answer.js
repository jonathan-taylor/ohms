/*
 *  This Source Code Form is subject to the terms of the Mozilla Public
 *  License, v. 2.0. If a copy of the MPL was not distributed with this
 *  file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 *  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>
 */

var OHMS = (function(OHMS) {

    var Answer = function (question) {
	this.element = this.element || null;
	this.question = question;
	this.create_element();
	this.element.data("answer",this);
	this.bind_events();
	if (this.solution !== undefined)
	    this.show_solution();
    }

    Answer.prototype.create_element = function () {
	this.element = $("<input type='text' name='ans' class='input-small' disabled='true'>");
    }

    Answer.prototype.bind_events = function () {
    }

    Answer.prototype.show_solution = function () {
    }

    Answer.prototype.get_value = function () {
	return this.element.val();
    }

    Answer.prototype.set_value = function (value) {
	this.element.val(value);
    }

    Answer.prototype.unlock_answer = function () {
	this.element.removeAttr("disabled");
    }

    Answer.prototype.lock_answer = function () {
	this.element.attr("disabled","disabled");
    }

    OHMS.Answer = Answer;

    return OHMS;

}(OHMS))
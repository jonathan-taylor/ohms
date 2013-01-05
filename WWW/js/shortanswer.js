/*
 *  This Source Code Form is subject to the terms of the Mozilla Public
 *  License, v. 2.0. If a copy of the MPL was not distributed with this
 *  file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 *  Copyright (c) 2012-2013, Dennis Sun <dlsun@stanford.edu>
 */

var OHMS = (function(OHMS) {

    var ShortAnswer = function(question, data) {
	this.text = data.text;
	this.max_pts = data.max_pts;
	this.solution = data.solution;
	OHMS.Answer.apply(this, arguments);
    }

    ShortAnswer.prototype = new OHMS.Answer();

    ShortAnswer.prototype.create_element = function () {
	this.element = $("<textarea class='Answer span6' rows=4 \
disabled/>");
    }

    ShortAnswer.prototype.show_solution = function () {
	this.element = null;
    }

    OHMS.ShortAnswer = ShortAnswer;

    return OHMS;

}(OHMS))
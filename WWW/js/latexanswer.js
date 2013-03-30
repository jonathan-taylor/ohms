var OHMS = (function(OHMS) {

    var LaTeXAnswer = function(question, data) {
	this.text = data.text;
	this.max_pts = data.max_pts;
	this.solution = data.solution;
	OHMS.Answer.apply(this, arguments);
    }

    LaTeXAnswer.prototype = new OHMS.Answer();

    LaTeXAnswer.prototype.bind_events = function () {
	var textbox = this.element.find("textarea");
	var preview = this.element.find(".preview");
	textbox.keyup(function() {
	    preview.text(textbox.val());
	    MathJax.Hub.Typeset(preview.get(0));
	});
    }

    LaTeXAnswer.prototype.create_element = function () {
	this.element = $(" \
<div class='Answer'> \
  <textarea class='span6' rows=4 disabled/> \
  <div><i>Live Preview</i></div> \
  <pre class='span6 preview'></pre> \
  <br> \
</div>");
    }

    LaTeXAnswer.prototype.show_solution = function () {
	this.element = null;
    }

    LaTeXAnswer.prototype.get_value = function () {
	return this.element.find("textarea").val();
    }

    LaTeXAnswer.prototype.set_value = function (value) {
	if (value !== null) {
	    this.element.find("textarea").val(value);
	    this.element.find(".preview").text(value);
	    MathJax.Hub.Typeset(this.element.find(".preview").get(0));
	}
    }

    LaTeXAnswer.prototype.unlock_answer = function () {
	this.element.find("textarea").removeAttr("disabled");
    }

    LaTeXAnswer.prototype.lock_answer = function () {
	this.element.find("textarea").attr("disabled","disabled");
    }

    OHMS.LaTeXAnswer = LaTeXAnswer;

    return OHMS;

}(OHMS))
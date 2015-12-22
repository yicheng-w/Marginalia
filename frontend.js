/** Nicely formats webpage.
 * 		Adds whitespace on either side of text.
 * 		Adds divs for notes and comments.
 */
var cleanPage = function cleanPage() {
	$("body").children().wrapAll("<div id='mar-text' />");  // original text
	$("body").prepend("<div id='mar-notes' />");			// left div for notes
	$("body").append("<div id='mar-comments' />");			// right div for comments
	$("body").children().css("float", "left");

	$("#mar-notes").css("width", "20%");
	$("#mar-notes").css("height", "50px");
	$("#mar-notes").css("background-color", "red");

	$("#mar-text").css("padding", "50px 0px 0px");
	$("#mar-text").css("width", "60%");

	$("#mar-comments").css("width", "20%"); 
	$("#mar-comments").css("height", "50px");
	$("#mar-comments").css("background-color", "red");
};

/** Formats comments and commented on sections of text.
 * 		Underlines commented on sections of text.
 */
var formatComments = function formatComments() {
	$(".comment").css("text-decoration", "underline");
};

/** Runs all necessary functions for Marginalia.
 */
var runMarginalia = function runMarginalia() {
	cleanPage();
	formatComments();
};
runMarginalia();



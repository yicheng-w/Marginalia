/*-----------------------------------------------------
 * Frontend javascript for the Annotation project. 
 * 
 * Authors
 *  Ariel Levy
 *
 * Description
 *  Formats article text, displays comments and notes.
 *
 *-----------------------------------------------------*/

/** TODO
 * 		Align comments with commented on text. -- see offset()
 * 		Highlight comment/commented text when hovering over partner. -- add unique comment id/classes shared by partners
 * 		Notes formatting.
 * 		Functionality to add comment.
 * 		Functionality to add notes.
 */

/** Dev Log
 * 		Basic Page Structure: 2015-12-20 13:00 - Ariel L.
 * 		Integration with Materialize: 2015-12-20 23:00 - Ariel L.
 */ 

/** Load Google Material Design files.
 */ 
var loadMaterialize = function loadMaterialize() {
	$("head").append("<link href='http://fonts.googleapis.com/icon?family=Material+Icons' rel='stylesheet'>");
	$("head").append("<link type='text/css' rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.4/css/materialize.min.css'  media='screen,projection'/>");
	$("head").append("<meta name='viewport' content='width=device-width, initial-scale=1.0'/>");
	$("body").append("<script type='text/javascript' href='https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.4/js/materialize.min.js'></script>");
};

/** Nicely formats webpage.
 * 		Adds whitespace on either side of text.
 * 		Adds divs for notes and comments.
 */
var cleanPage = function cleanPage() {
	$("body").children().wrapAll("<div id='mar-text' />");  // original text
	$("body").prepend("<div id='mar-notes' />");			// left div for notes
	$("body").append("<div id='mar-comments' />");			// right div for comments

	$("body").addClass("grey lighten-3");
	$("body").children().wrapAll("<div class='row' />");
	loadMaterialize();

	$("#mar-notes").addClass("col s4");
	$("#mar-notes").css("min-height", "100vh");

	$("#mar-text").addClass("col s4 white");

	$("#mar-comments").addClass("col s4");
	$("#mar-comments").css("min-height", "100vh");
};

/** Formats comments and commented on sections of text.
 * 		Underlines commented on sections of text.
 * 		Moves user comments to comment div.
 * 		Removes comments from the body of the article.
 */
var formatComments = function formatComments() {
	$(".comment").css("text-decoration", "underline");
	var colors = ["pink", "indigo", "cyan", "light-green", "deep-orange"];
	var i = 0;
	$(".comment").each(function() {
		var col = colors[i%5]; 
		var c = "<div class='comment-block white-text darken-4 "+col+"'>";
	   	c += $(this).find(".comment-text").text();
		c += "</div>";
		$("#mar-comments").append(c);
		$(this).addClass(col+"-text text-darken-4");
		i++;
	})
	$("#mar-text .comment-text").remove();
	
	$(".comment-block").addClass("card-panel hoverable");
};

/** Runs all necessary functions for Marginalia.
 */
var runMarginalia = function runMarginalia() {
	cleanPage();
	formatComments();
};
runMarginalia();

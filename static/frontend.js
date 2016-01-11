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
 * 		Highlight comment/commented text when hovering over partner. -- add unique comment id/classes shared by partners
 * 		Scrollfire for comments.
 * 		Functionality to add comment.
 */

/** Dev Log
 * 		Basic Page Structure: 2015-12-20 13:00 - Ariel L.
 * 		Integration with Materialize: 2015-12-20 23:00 - Ariel L.
 * 		Note and Comment Structure: 2015-12-28 17:00 - Ariel L.
 */ 

/** Nicely formats webpage.
 * 		Adds whitespace on either side of text.
 * 		Adds divs for notes and comments.
 */
var cleanPage = function cleanPage() {
	$("#content").children().wrapAll("<div id='mar-text' />");  // original text
	$("#content").prepend("<div id='mar-notes' />");			// left div for notes
	$("#content").append("<div id='mar-comments' />");			// right div for comments

	$("#content").addClass("grey lighten-3");
	$("#content").children().wrapAll("<div class='row' />");

	$("#mar-notes").addClass("col s4");
	$("#mar-notes").css("min-height", "100vh");

	$("#mar-text").addClass("col s4 white");

	$("#mar-comments").addClass("col s4");
	$("#mar-comments").css("min-height", "100vh");
};

/** Formats comments and commented on sections of text.
 * 		Underlines commented on sections of text.
 * 		Color codes comments and text sections.
 * 		Lines up comments and text sections.
 */
var formatComments = function formatComments() {
	var colors = ["pink", "indigo", "cyan", "light-green", "deep-orange"];
	var i = 0;
	$(".comment").each(function() {
		var ctag = "com-"+i;
		var col = colors[i%5]; 
		$(this).addClass(col+"-text text-darken-4 "+ctag);
		i++;
	})
	i = 0;
	$(".comment-block").each(function() {
		var ctag = "com-"+i;
		var col = colors[i%5];
		$(this).addClass(col+" "+ctag);
		i++;
	})
	
	var tbaseOffset = $("#mar-text").offset()["top"];	   // top of the text column
	var cbaseOffset = $("#mar-comments").offset()["top"];  // top of the comment column
	i = 0;
	var textOffsets = [];
	var origOffsets = []; 
	$(".comment").each(function() {
		var ctag = "com-"+i;
		origOffsets[i] = $("#mar-comments").find("."+ctag).offset()["top"];  // original offset from top of column
		textOffsets[i] = $("#mar-text").find("."+ctag).offset()["top"];      // offset of commented on text
		i++;
	})	
	i = 0;
	
	$(".comment").each(function() {
		if (i == 0) {
			$("#mar-comments").find(".com-0").offset({"top":cbaseOffset-tbaseOffset+textOffsets[0]});
		}
		else {
			var prevDif = origOffsets[i] - origOffsets[i-1];
			var textDif = textOffsets[i] - textOffsets[i-1];
			if (textDif > prevDif) {
				var init = $("#mar-comments").find(".com-"+(i-1)).offset()["top"];
				$("#mar-comments").find(".com-"+i).offset({"top":init+textDif});
			}
		}
		i++;
	})
	
};

/** Function to animate "Add Note" button.
 * 		Button slides left.
 * 		Shortens to just icon.
 * 		Changes ID to '#write-note'.
 */
var showInput = false;
var clickAddNote = function clickAddNote() {
	$("#add-note").click(function() {
		if ( !showInput ) {
			$("#add-note")[0].type = 'submit';
			$("#add-note").html('<i class="material-icons right">create</i>');
			$("#add-note").find("i").removeClass("right");
			var b = "<button class='btn waves-effect waves-light red' type='button' name='action' id='clear-note'>";
			b += "<i class='material-icons'>clear</i></button>";
			$("#add-note").after(b);
			clickClearNote();
			var t = "<div class='row' id='note-input'>";
			t += "<form class='col s12'>";
			t += "<div class='row'>";
			t += "<div class='input-field col s12'>";
			t += "<textarea id='note-text' class='materialize-textarea' placeholder='Note'></textarea>";
			t += "</div></div></form></div>";
			$("#mar-notes").prepend(t);
			showInput = true;
		}
		else {
			var newNote = $("#note-text").val();
			if ( newNote.trim() ) {  // note is not empty
				$("#note-list").append("<li>"+newNote+"</li>");
			}
			$("#add-note")[0].type = 'button';
			$("#add-note").html('Add Note<i class="material-icons right">create</i>');
			$("#add-note").find("i").addClass("right");
			$("#note-input").remove();
			$("#clear-note").remove();
			showInput = false;
		}
	});
};

var clickClearNote = function clickClearNote() {
	$("#clear-note").click(function() {
		console.log("exec");
		$("#add-note")[0].type = 'button';
		$("#add-note").html('Add Note<i class="material-icons right">create</i>');
		$("#add-note").find("i").addClass("right");
		$("#note-input").remove();
		$("#clear-note").remove();
		showInput = false;
	});
};
	

/** Runs all necessary functions for Marginalia.
 */
var runMarginalia = function runMarginalia() {
//	cleanPage();
	formatComments();
	clickAddNote();
//	clickClearNote();
};
runMarginalia();

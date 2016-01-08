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
 * 		Fix comment overlapping.
 * 		Scrollfire for comments.
 * 		Saving notes.
 * 		Functionality to add comment.
 */

/** Dev Log
 * 		Basic Page Structure: 2015-12-20 13:00 - Ariel L.
 * 		Integration with Materialize: 2015-12-20 23:00 - Ariel L.
 * 		Note and Comment Structure: 2015-12-28 17:00 - Ariel L.
 * 		Hover Highlighting: 2016-01-08 10:09 - Ariel L.
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
	var colors = ["pink", "indigo", "purple", "light-blue", "teal"];
	var i = 0;
	$(".comment").each(function() {
		var ctag = "com-"+i;
		var col = colors[i%5]; 
		$(this).addClass(col+"-text text-darken-3 "+ctag);
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
	var location_avaliable = Array($('#mar-comments').height());

	for (var j = 0 ; j < $("#mar-comments").height() ; j++) {
        location_avaliable[j] = 0;
    }

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
			for (var j = 0 ; j < $("#mar-comments").find(".com-0").height() ; j++) {
    			location_avaliable[textOffsets[0] + j] = 1;
            }
		}
		else {
			var prevDif = origOffsets[i] - origOffsets[i-1];
			var textDif = textOffsets[i] - textOffsets[i-1];
			if (textDif > prevDif) {
				var init = $("#mar-comments").find(".com-"+(i-1)).offset()["top"];
				var tentative = init+textDif;

				while (location_avaliable[tentative] == 1) { // while the spot is occupied
                    tentative++; // move down
                }
				$("#mar-comments").find(".com-"+i).offset({"top":tentative});

				console.log("comment");
				console.log(tentative);
				console.log(tentative + $("mar-comments").find(".com-"+i).height());

				for (var j = 0 ; j < $("mar-comments").find(".com-"+i).height() ; j++) {
                    location_avaliable[tentative + j] = 1;
                }
			}

			//console.log(location_avaliable);
		}
		i++;
	})
	
};

/** Formats comment and comment block when hovered over.
 *		Highlights comment in grey.
 *		Makes comment block italic and gives it depth.
 */
var commentHoverOn = function commentHoverOn(num) {
	var ctag = ".com-"+num;
	$(".comment"+ctag).addClass("grey lighten-2");
	$(".comment-block"+ctag).css("font-style","italic");
	$(".comment-block"+ctag).addClass("z-depth-5");
};

/** Undos hover formatting for comment and comment block.
 */	
var commentHoverOff = function commentHoverOff(num) {
	var ctag = ".com-"+num;
	$(".comment"+ctag).removeClass("grey lighten-2");
	$(".comment-block"+ctag).css("font-style","normal");
	$(".comment-block"+ctag).removeClass("z-depth-5");
};

/** Adds hover command to comments and comment blocks.
 */
var hoverAll = function hoverAll() {
	var len = $(".comment").length;
	$(".comment").each(function() {
		var className = $(this).attr('class');
		var num = className[className.length-1];
		$(this).hover(function() {
			commentHoverOn(num);
		},function() {
			commentHoverOff(num);
		})
	})
	$(".comment-block").each(function() {
		var className = $(this).attr('class');
		var num = className[className.length-1];
		$(this).hover(function() {
			commentHoverOn(num);
		},function() {
			commentHoverOff(num);
		})
	})
};

var getSelectedText = function getSelectedText() {
    var text = "";
	if (window.getSelection) {
		text = window.getSelection().toString();
	} else if (document.selection && document.selection.type != "Control") {
		text = document.selection.createRange().text;
	}
	console.log(text);
	return text;
};

var addCommentOption = function addCommentOption() {
	var selectedText = getSelectedText();
	if (selectedText) {
//		alert("Got selected text " + selectedText);
//
	}
}

//document.onmouseup = doSomethingWithSelectedText;
//document.onkeyup = doSomethingWithSelectedText;
	

/** Runs all necessary functions for Marginalia.
 */
var runMarginalia = function runMarginalia() {
//	cleanPage();
	formatComments();
	hoverAll();
	getSelectedText();
};
runMarginalia();

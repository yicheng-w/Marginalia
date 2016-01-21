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
 * 		Scrollfire for comments.
 * 		Saving notes.
 * 		Debug multiple comment adding.
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

var href = window.location.href;
console.log(href);
var site_id = parseInt(href.substr(href.lastIndexOf('/') + 1), 10);

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
		var oldCol;
	   	if (i == 0) {
			oldCol = colors[4];
		}
		else {
			oldCol = colors[(i-1)%5];
		}
		$(this).removeClass(oldCol+"-text");
		$(this).addClass(col+"-text text-darken-3 "+ctag);
		i++;
	})
	i = 0;
	$(".comment-block").each(function() {
		$(this).removeClass("black");
		var ctag = "com-"+i;
		var col = colors[i%5];
		var oldCol;
	   	if (i == 0) {
			oldCol = colors[4];
		}
		else {
			oldCol = colors[(i-1)%5];
		}
		$(this).removeClass(oldCol);
		$(this).addClass(col+" "+ctag);
		i++;
	})
	
	var location_avaliable = Array($(window).height());

	for (var j = 0 ; j < location_avaliable.length ; j++) {
        location_avaliable[j] = 0;
    }

	i = 0;

	var textOffsets = [];

	$(".comment").each(function() {
		var ctag = "com-"+i;
		textOffsets[i] = Math.round($('.comment.'+ctag).offset().top);      // offset of commented on text
		i++;
	})
	i = 0;

	$(".comment").each(function() {

	    while (location_avaliable[textOffsets[i]] == 1) {
            textOffsets[i]++;
        }

	    $('.comment-block.com-'+i).offset({"top" : textOffsets[i]});

	    for (var j = 0 ; j < $('.comment-block.com-'+i).height() + 50 ; j++) {
            location_avaliable[textOffsets[i] + j] = 1;
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
	$(".comment-block"+ctag).addClass("z-depth-5");
	$(".comment-block"+ctag).animate({
		opacity: "1"
	}, "fast")
};

/** Undos hover formatting for comment and comment block.
 */	
var commentHoverOff = function commentHoverOff(num) {
	var ctag = ".com-"+num;
	$(".comment"+ctag).removeClass("grey lighten-2");
	$(".comment-block"+ctag).removeClass("z-depth-5");
	$(".comment-block"+ctag).animate({
		opacity: "0.85"
	}, "fast")
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

var insertComment = function insertComment() {
	var newCom = $(".comment.new-com");
	var newInd = $(".comment").index(newCom);
	var newBlock = $(".comment-block.new-com");
	$(".mar-comments").remove(".new-com");
	if (newInd == 0) {
		$(".comment-block.com-0").before(newBlock);
	}
	else {
		$(".comment-block.com-"+(newInd-1)).after(newBlock);
	}
	$(".new-com").removeClass("new-com");
	
	// clear original indices and hovering 
	var i = 0;
	$(".comment").each(function() {
		$(this).removeClass("com-"+i);
		$(this).removeClass("com-"+(i-1));
		$(this).unbind("mouseenter mouseleave");
		i++;
	});
	i = 0;
	$(".comment-block").each(function() {
		$(this).removeClass("com-"+i);
		$(this).removeClass("com-"+(i-1));
		$(this).unbind("mouseenter mouseleave");
		i++;
	});

	formatComments();
	hoverAll();
};

var addCommentOption = function addCommentOption( st ) {
	$("#com-on").text( st );
	$("#add-com").css("visibility", "visible");
}

var addComment = function addComment(text) {
	$("#mar-comments").append("<div class='comment-block white-text darken-3 black card-panel hoverable new-com'>"+text+"</div>");
};

var surround = function(textNode, surroundings) {
    if (textNode.rangeCount) {
        var range = textNode.getRangeAt(0).cloneRange();
        range.surroundContents(surroundings);
        textNode.removeAllRanges();
        textNode.addRange(range);
        return true;
    }
    return false;
}

var addCommentMaster = function(selectedText) {
    var spanText = document.createElement("span");
    spanText.classList.add("comment");
    spanText.classList.add("new-com");
    surround(selectedText, spanText);
    addCommentOption( selectedText );
    $('#cursor_menu').css('visibility', 'hidden');
    save_site();
}

var highlight = function(selectedText) {
    if (selectedText.rangeCount) {
        var parentEl = selectedText.getRangeAt(0).commonAncestorContainer;
        if (parentEl.nodeType != -1) {
            parentEl = parentEl.parentNode;
        }
    }

    if (parentEl.classList.contains("highlight")) {
        // if it is already highlighted, this function shall unhighligt
        var pparent = parentEl.parentNode;
        while (parentEl.firstChild) pparent.insertBefore(parentEl.firstChild, parentEl);
        pparent.removeChild(parentEl);
    }
    else { // otherwise highlight it
        var spanText = document.createElement("span");
        spanText.classList.add("highlight");
        surround(selectedText, spanText);
    }
    $('#cursor_menu').css('visibility', 'hidden');
    save_site();

}

$("#mar-text").on("mouseup",function(f) {
	var selectedText = window.getSelection();
	if (selectedText.toString()) {
	    console.log(selectedText.toString());
		$(document).keydown(function(e) {
			if (e.keyCode == 67 && e.ctrlKey && e.altKey) { // comment
			    addCommentMaster(selectedText);
			}
            else if (e.keyCode == 72 && e.ctrlKey && e.altKey) { // highlight
                highlight(selectedText);
            }
		});
		$('#cursor_menu').css('visibility', 'visible');
		$('#cursor_menu').offset({
            left: f.pageX + 20,
            top: f.pageY
        });
	}
	else {
	    $("#cursor_menu").css('visibility', 'hidden');
        $(document).off('keydown');
	}
});

$('#add-com-b').on('click', function() {
    var selectedText = window.getSelection();
    if (selectedText) {
        addCommentMaster(selectedText);
    }
});

$('#add-hi').on('click', function() {
    var selectedText = window.getSelection();
    if (selectedText) {
        highlight(selectedText);
    }
})

$("#kill-com").on("click",function() {
	var uncomText = $(".new-com").text();
	$(".new-com").after( uncomText );
	$(".new-com").remove();
	$("#com-text").val("");
	$("#add-com").css("visibility", "hidden");
});

$("#save-com").on("click",function() {
	var comText = $("#com-text").val();	
	console.log(comText);
	addComment(comText);
	insertComment();
	$("#com-text").val("");
	$("#add-com").css("visibility", "hidden");
	save_site();
});

$("#save-notes").on("click", function() {
    save_site();
});

/** Runs all necessary functions for Marginalia.
 */
var runMarginalia = function runMarginalia() {
//	cleanPage();
	formatComments();
	hoverAll();
};

runMarginalia();

var save_site = function save() {
	var site = {
        'site': document.getElementById("mar-text").innerHTML,
        'comment': document.getElementById("mar-comments").innerHTML,
        'note': document.getElementById("note-panel").value
    };
    $.post("/update/" + site_id, site, function(data) {
        Materialize.toast("Comments saved!", 1000);
    },"json");
}

function getOffset( el ) {
    var rect = el.getBoundingClientRect();
    return {
        left: rect.left + window.pageXOffset,
        top: rect.top + window.pageYOffset,
        width: rect.width || el.offsetWidth,
        height: rect.height || el.offsetHeight
    };
}

function connect(div1, div2, thickness) { // draw a line connecting elements
    var off1 = getOffset(div1);
    var off2 = getOffset(div2);
    // bottom right
    var x1 = off1.left + off1.width;
    var y1 = off1.top + off1.height;
    // top right
    var x2 = off2.left + off2.width;
    var y2 = off2.top;
    // distance
    var length = Math.sqrt(((x2-x1) * (x2-x1)) + ((y2-y1) * (y2-y1)));
    // center
    var cx = ((x1 + x2) / 2) - (length / 2);
    var cy = ((y1 + y2) / 2) - (thickness / 2);
    // angle
    var angle = Math.atan2((y1-y2),(x1-x2))*(180/Math.PI);
    // make hr
    var htmlLine = "<div style='padding:0px; margin:0px; height:" + thickness + "px; background-color:#000" + "; line-height:1px; position:absolute; left:" + cx + "px; top:" + cy + "px; width:" + length + "px; -moz-transform:rotate(" + angle + "deg); -webkit-transform:rotate(" + angle + "deg); -o-transform:rotate(" + angle + "deg); -ms-transform:rotate(" + angle + "deg); transform:rotate(" + angle + "deg);' />";
    //
    // alert(htmlLine);
    document.body.innerHTML += htmlLine;
}

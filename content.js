/*-----------------------------------------------------------------------------
 * Content Script
 *
 * Authors
 *  Alice Xue, Jeffrey Zou
 *
 * Description
 *  Runs in the context of the webpage, makes changes to the webpage
 *
 *-----------------------------------------------------------------------------*/


console.log("loaded content.js");

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
	console.log(request);
	console.log(sender);
	console.log(sendResponse);
        if(request.method == "getHTML"){
	    var metadata = document.getElementsByTagName("meta");
	    var divs = document.getElementsByTagName("div");
	    var spans = document.getElementsByTagName("span");
            var paragraphs = document.getElementsByTagName("p");
            var title = document.title;
	    var dates = document.getElementsByTagName("time");
	    var datePublished = "";
	    if (typeof dates[0] != "undefined") {
		datePublished = dates[0].innerText;
	    }
	    for (i=0;i<dates.length;i++) {
		if (dates[i].getAttribute("itemprop") == "datePublished") {
		    datePublished = dates[i].innerText;
		}
	    }
	    if (datePublished == "") {
		for (i=0;i<metadata.length;i++) {
		    if (metadata[i].getAttribute("property") == "article:published_time") {
			datePublished = metadata[i].getAttribute("content");
			if (datePublished.length > 10) {
			    datePublished = datePublished.substring(0,10);
			}
		    }
		}
	    }
	    console.log(datePublished);
	    var author = "";
	    for (i=0;i<metadata.length;i++) {
		if (metadata[i].getAttribute("name") == "author") {
		    author = metadata[i].getAttribute("content");
		    break;
		}
	    }
	    if (author == "") {
		for (i=0;i<spans.length;i++) {
		    if (spans[i].class == "byline-author") {
			author = spans[i].innerText;
			break;
		    }
		}
	    }
	    if (author == "") {
		var anchors = document.getElementsByTagName("a");
		for (i=0;i<anchors.length;i++) {
		    if (anchors[i].getAttribute("itemprop") == "author") {
			author = anchors[i].innerText;
		    }
		}
	    }
	    console.log(author);
            var onlyP = [];
            var pText = [];
            for (i=0;i<paragraphs.length;i++) {
		if (paragraphs[i].getAttribute("itemprop") == "articleBody") {
		    onlyP.push(paragraphs[i]);
		    //Take the text and put it into array
		    //NOTE: Firefox does NOT support innerText!
		    pText.push(paragraphs[i].innerHTML);
		}
            }
	    if (pText.length == 0) {
		for (i=0;i<divs.length;i++) {
		    if (divs[i].getAttribute("itemprop") == "articleBody" || divs[i].getAttribute("id") == "article-body") {
			divParagraphs = divs[i].children;
			console.log(divParagraphs);
			for (j=0;j<divParagraphs.length;j++) {
			    if (divParagraphs[j].tagName == "P") {
				console.log(divParagraphs[j]);
				console.log(divParagraphs[j].tagName);
				onlyP.push(divParagraphs[j]);
				pText.push(divParagraphs[j].innerHTML);
			    }
			}
		    }
		}
	    }
	    if (pText.length == 0) {
		for (i=0;i<spans.length;i++) {
		    if (spans[i].class == "s1") {
			onlyP.push(spans[i]);
			pText.push(spans[i].innerHTML);
		    }
		}
	    }
	    
            //console.log("--------------------------");
            console.log("---------title------------");
            console.log(title);
	    
	    
	    
            console.log("-------Paragraphs---------");
            console.log(pText);
            var data = {
		title:title,
		p:paragraphs,
		method:"getHTML"
          };
            sendResponse(data);
        }
    }
);

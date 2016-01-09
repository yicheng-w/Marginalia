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
            console.log(document.getElementsByTagName("p"));
	    var divs = document.getElementsByTagName("div");
            var paragraphs = document.getElementsByTagName("p");
            var title = document.title;
            var onlyP = [];
            var pText = [];
            for (i=0;i<paragraphs.length;i++) {
		if (paragraphs[i].getAttribute("itemprop") == "articleBody") {
		    onlyP.push(paragraphs[i]);
		    //Take the text and put it into array
		    //NOTE: Firefox does NOT support innerText!
		    pText.push(paragraphs[i].innerText);
		}
            }
	    for (i=0;i<divs.length;i++) {
		if (divs[i].getAttribute("itemprop") == "articleBody") {
		    divParagraphs = divs[i].children;
		    console.log(divParagraphs);
		    for (j=0;j<divParagraphs.length;j++) {
			if (divParagraphs[j].tagName == "P") {
			    onlyP.push(divParagraphs[j]);
			    pText.push(divParagraphs[j].innerText);
			}
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

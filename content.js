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
          //console.log(document.getElementsByTagName("p"));
          var paragraphs = document.getElementsByTagName("p");
          var onlyP = [];
          var pText = [];
          for (i=0;i<paragraphs.length;i++) {
            if (paragraphs[i].classList.length == 0) {
                onlyP.push(paragraphs[i]);
                //Take the text and put it into array
                //NOTE: Firefox does NOT support innerText!
                pText.push(paragraphs[i].innerText);
            }
          }
          console.log("--------------------------");
          console.log(pText);
          sendResponse({data: document.getElementsByTagName("p"),  method: "getHTML"});
	    //console.log(document.body.outerHTML);
            //sendResponse({data: document.body.outerHTML,  method: "getHTML"});
        }
    }
);

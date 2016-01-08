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
          var title = document.title;
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

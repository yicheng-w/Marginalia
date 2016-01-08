console.log("loaded content.js");

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
	console.log(request);
	console.log(sender);
	console.log(sendResponse);
        if(request.method == "getHTML"){
          console.log(document.getElementsByTagName("p"));
          var paragraphs = document.getElementsByTagName("p");
          var onlyP = [];
          for (i=0;i<paragraphs.length;i++) {
            console.log(paragraphs[i].classList.length == 0);
            }
          //console.log(onlyP);
          sendResponse({data: document.getElementsByTagName("p"),  method: "getHTML"});
	    //console.log(document.body.outerHTML);
            //sendResponse({data: document.body.outerHTML,  method: "getHTML"});
        }
    }
);

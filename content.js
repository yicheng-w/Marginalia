console.log("loaded content.js");

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
	console.log(request);
	console.log(sender);
	console.log(sendResponse);
        if(request.method == "getHTML"){
	    console.log(document.body.outerHTML);
            sendResponse({data: document.body.outerHTML,  method: "getHTML"});
        }
    }
);

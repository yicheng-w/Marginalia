console.log("loaded content.js");

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if(request.method == "getHTML"){
	    console.log(document.all[0].innerText);
            sendResponse({data: document.all[0].innerText,  method: "getHTML"});
        }
    }
);

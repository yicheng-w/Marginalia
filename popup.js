console.log("loaded popup.js");

chrome.tabs.query({active: true}, function(tabArray) {
    currentTabID = tabArray[0].id;
    chrome.tabs.sendMessage(currentTabID, {method: "getHTML"}, function(response) {
        if(response.method=="getHTML"){
	    console.log(currentTabID);
            alltext = response.data;
	    console.log(alltext);
        }
    });
});

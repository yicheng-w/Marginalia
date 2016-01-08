/*-----------------------------------------------------------------------------
 * Popup Script
 *
 * Authors
 *  Alice Xue, Jeffrey Zou
 *
 * Description
 *  Receives HTML from content.js when the extension is clicked
 *
 *-----------------------------------------------------------------------------*/

console.log("loaded popup.js");

chrome.tabs.query({currentWindow: true, active: true}, function(tabArray) {
    currentTabID = tabArray[0].id;
    chrome.tabs.sendMessage(currentTabID, {method: "getHTML"}, function(response) {
        if(response.method=="getHTML"){
	         console.log(currentTabID);
           alltext = response.p;
           title = response.title;
	         console.log(alltext);
        }
    });
});

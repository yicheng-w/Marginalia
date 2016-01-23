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
            html = response.p;
            title = response.title;
	    author = response.author;
	    date = response.date;
	    url = response.url;
	    var send = function() {
		var request = new XMLHttpRequest();
		request.open("POST", "http://localhost:8000/new/", true);
		request.setRequestHeader('Content-type','application/x-www-form-urlencoded');
		request.send('title='+encodeURIComponent(title)+'&author='+encodeURIComponent(author)+'&date='+encodeURIComponent(date)+'&url='+url+'&site=' + encodeURIComponent(html));
	    }
	    send();
        }
    });
});

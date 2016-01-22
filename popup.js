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
	    var send = function() {
		var url = "parseHTML.py";
		var request = new XMLHttpRequest();
		/*
		  request.onreadystatechange = function(){
		  if (request.readyState === 4 && request.status === 200) {
		  alert('worked');
		  } else if (request.readyState == 4) {
		  alert('did not work :(' + request.status);
		  }
		  }
		*/
		request.open("POST", "http://localhost:8000/new/", true);
		request.setRequestHeader('Content-type','application/x-www-form-urlencoded');
		request.send('title='+encodeURIComponent(title)+'&author='+encodeURIComponent(author)+'&date='+encodeURIComponent(date)+'&site=' + encodeURIComponent(html));
	    }
	    send();
        }
    });
});

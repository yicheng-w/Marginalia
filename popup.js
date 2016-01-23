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

var viewBase = "http://localhost:8000/view/";
var id = '0';

document.getElementById('link').addEventListener('click', function() {
    window.open(viewBase + id);
});

chrome.tabs.query({currentWindow: true, active: true}, function(tabArray) {
    currentTabID = tabArray[0].id;
    chrome.tabs.sendMessage(currentTabID, {method: "getHTML"}, function(response) {
        if(response.method=="getHTML"){
            html = response.p;
            title = response.title;
	    author = response.author;
	    date = response.date;
	    var send = function() {
		//var url = "parseHTML.py";
		var request = new XMLHttpRequest();
		request.open("POST", "http://localhost:8000/new/", true);
		request.setRequestHeader('Content-type','application/x-www-form-urlencoded');
		request.send('title='+encodeURIComponent(title)+'&author='+encodeURIComponent(author)+'&date='+encodeURIComponent(date)+'&site=' + encodeURIComponent(html));
		request.onreadystatechange = function() {
            if (request.readyState == 4) {
                console.log(request.response);
                if (request.response == 'failure') {
                    document.getElementById('status').innerHTML = "The page could not be added, something went wrong";
                }
                else if (request.response == 'login') {
                    document.getElementById('status').innerHTML = "Please log in";
                    window.open("http://localhost:8000/login");
                }
                else {
                    document.getElementById('status').innerHTML = "<b>Added to Marginalia!</b>";
                    id = request.response;
                    document.getElementById('link').style.visibility = 'visible';
                }
            }
        }
	    }
	    send();
        }
    });
});

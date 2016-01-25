/*-----------------------------------------------------------------------------
 * Popup Script
 *
 * Authors
 *  Alice Xue, Jeffrey Zou, Yicheng Wang
 *
 * Description
 *  Receives HTML from content.js when the extension is clicked
 *
 *-----------------------------------------------------------------------------*/

console.log("loaded popup.js");

var viewBase = "http://marginalia.alex-wyc.me/view/";
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
	    url = response.url;
	    var send = function() {
		var request = new XMLHttpRequest();
		request.open("POST", "http://104.236.86.43:8000/new/", true);
		request.setRequestHeader('Content-type','application/x-www-form-urlencoded');
		request.send('title='+encodeURIComponent(title)+'&author='+encodeURIComponent(author)+'&date='+encodeURIComponent(date)+'&url='+url+'&site=' + encodeURIComponent(html));
        document.getElementById('status').innerHTML = "Cleaning the website... Please wait...";
		request.onreadystatechange = function() {
            if (request.readyState == 4) {
                console.log(request.response);
                if (request.response == 'failure') {
                    document.getElementById('status').innerHTML = "The page could not be added, something went wrong";
                }
                else if (request.response == 'login' || request.response == '') {
                    document.getElementById('status').innerHTML = "Please log in";
                    window.open("http://marginalia.alex-wyc.me/login");
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

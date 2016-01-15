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
  	    var metadata = document.getElementsByTagName("meta");
  	    var divs = document.getElementsByTagName("div");
        //var paragraphs = document.getElementsByTagName("p");
        var title = document.title;
  	    var datePublished = "";

  	    dates = document.querySelectorAll("time, [itemprop=datePublished], span[class=timeago], span[class=timestamp]");
  	    authors = document.querySelectorAll("[name=author], .byline-author, [itemprop=author], h3[class=article-author-title] > a");
  	    paragraphs = document.querySelectorAll("p[itemprop=articleBody], p[class=p1], div[itemprop=articleBody] > p, div[id=article-body] > p, div[class=article-entry] > p, span[class=focusParagraph] > p, span[id=articleText] > p");

  	    for (i=0;i<dates.length;i++) {
  		      datePublished = dates[i].innerText;
  		      if (typeof datePublished == "undefined" || datePublished == "" || datePublished == null) {
  		          datePublished = dates[i].getAttribute("content");
  		      }
  		      if (typeof datePublished != "undefined" & datePublished != "" & datePublished != null) {
  		          break;
  		      }
  	    }

        var that = document.body.outerHTML;
  	    console.log("---------------------------------------------------------");
        console.log(typeof that);
        console.log("---------------------------------------------------------");
  	    var author = "";
  	    for (i=0;i<authors.length;i++) {
  		      author = authors[i].innerText;
  		      if (typeof author == "undefined" || author == "" || author == null) {
  		          author = authors[i].getAttribute("content");
  		      }
		        if (typeof author != "undefined" & author != "" & author != null) {
		            break;
		        }
	      }

	      if (datePublished == "") {
		        for (i=0;i<metadata.length;i++) {
		            if (metadata[i].getAttribute("property") == "article:published_time") {
			               datePublished = metadata[i].getAttribute("content");
			               if (datePublished.length > 10) {
			                    datePublished = datePublished.substring(0,10);
			              }
		            }
		        }
	      }

        var onlyP = [];
        var pText = [];


	    for (i=0;i<paragraphs.length;i++) {
		      if (paragraphs[i].tagName == "P") {
		          onlyP.push(paragraphs[i]);
		          pText.push(paragraphs[i].innerHTML);
		      }
	    }
	    if (pText.length == 0) {
		      for (i=0;i<divs.length;i++) {
		          divParagraphs = divs[i].children;
		          for (j=0;j<divParagraphs.length;j++) {
			             if (divParagraphs[j].tagName == "P") {
			                  onlyP.push(divParagraphs[j]);
			                  pText.push(divParagraphs[j].innerHTML);
			              }
			              if (divParagraphs[j].tagName == "SECTION") {
			                   sectionParagraphs = divParagraphs[j].children;
			                   for (k=0;k<sectionParagraphs.length;k++) {
				                       onlyP.push(sectionParagraphs[k]);
				                       pText.push(sectionParagraphs[k].innerHTML);
			                  }
			              }
		          }
		      }
	    }


      var send = function() {
        var url = "parseHTML.py";
        var request = new XMLHTTPRequest();
        /*request.onreadystatechange = function(){
          if (request.readyState === 4 && request.status === 200) {

          }
        }*/
        request.open("POST", "parseHTML.py?data=" + paragraphs, true);
        request.send(document.html);
        console.log("SUCCESS");
      }

      //console.log("--------------------------");
      console.log("---------title------------");
      console.log(title);
	    console.log("---------Date------------");
	    console.log(datePublished);
	    console.log("---------Author------------");
	    console.log(author);


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

selectedkey = 0;

function searchsuggestion(input, key) {

	div = document.getElementById("searchsuggestions");
	if (key == 40) {
		selectedkey++;
		Selectsuggestion(selectedkey)
		return;
	}
	if (key == 38) {
		selectedkey--;
		Selectsuggestion(selectedkey)
		return;
	}

	selectedkey = 0;

	searchstring = input.value;
	req = new XMLHttpRequest();
	req.open("POST","/searchsuggestions",true);
	req.setRequestHeader("Content-type","application/x-www-form-urlencoded ");
	req.send("search=" + searchstring);

	req.onreadystatechange= function() {
		if (req.readyState==4) {
			if (req.status==200) {
				div.innerHTML = req.responseText;
				div.style.visibility = "visible";
			}
		}

	}
}

function hideSuggestions() {
	setTimeout('document.getElementById("searchsuggestions").style.visibility = "hidden"', 250)
}

function Selectsuggestion(idx) {

	var div = document.getElementById("searchsuggestions");
	links = div.getElementsByTagName("a");
	if (selectedkey > links.length) {
		selectedkey = links.length;
		idx = links.length;
	}
	if (selectedkey < 1) {
		selectedkey = 1;
		idx = 1;
	}
	for (i = 1; i <= links.length; i++) {
		if (i == idx) {
			links[i-1].selected = true;
			links[i-1].style.background = "white";
		} else {
			links[i-1].selected = false;
			links[i-1].style.background = "transparent";
		}
	}

}

function keypress(key) {
	if (key == 13) {
		links = document.getElementById("searchsuggestions").getElementsByTagName("a");
		for (i = 0; i <= links.length-1; i++) {
			if (links[i].selected == true) {
				document.location.href = links[i].href;
				return false;
			}
		}

	}
}
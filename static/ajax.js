
function request_visual_code(host_tag) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4)
	{
		if (this.status == 200)
			document.getElementById(host_tag).innerHTML = this.responseText;
		else
			document.getElementById(host_tag).innerHTML = this.status.toString() + " Error"
    }
  };
  var request_url = "addvial?tissue=" + document.getElementById("tissue").value;
  request_url	 += "&donner=" + document.getElementById("donner").value;
  request_url	 += "&vialnum=" + document.getElementById("vialnum").value;
  request_url	 += "&passage=" + document.getElementById("passage").value;
  request_url	 += "&date_yy=" + document.getElementById("date_yy").value;
  request_url	 += "&date_mm=" + document.getElementById("date_mm").value;
  request_url	 += "&date_dd=" + document.getElementById("date_dd").value;
  request_url	 += "&location=" + document.getElementById("location").value;
  request_url	 += "&number=" + document.getElementById("number").value;
  xhttp.open("GET", request_url, true);
  document.getElementById(host_tag).innerHTML = "Generating visual code...";
  xhttp.send();
}

function fetch_visual_code(host_tag) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4)
	{
		if (this.status == 200)
		{
			document.getElementById(host_tag).innerHTML = this.responseText;
			$(".vial_query").tablesorter({
				theme : 'blue', 
				sortList : [[0,0]]
			});
		}
		else
			document.getElementById(host_tag).innerHTML = this.status.toString() + " Error"
    }
  };
  var request_url = "findvial?tissue=" + document.getElementById("tissue").value;
  request_url	 += "&donner=" + document.getElementById("donner").value;
  request_url	 += "&vialnum=" + document.getElementById("vialnum").value;
  request_url	 += "&passage=" + document.getElementById("passage").value;
  request_url	 += "&date_yy=" + document.getElementById("date_yy").value;
  request_url	 += "&date_mm=" + document.getElementById("date_mm").value;
  request_url	 += "&date_dd=" + document.getElementById("date_dd").value;
  request_url	 += "&location=" + document.getElementById("location").value;
  request_url	 += "&number=" + document.getElementById("number").value;
  xhttp.open("GET", request_url, true);
  document.getElementById(host_tag).innerHTML = "Querying codes...";
  xhttp.send();
}

function remove_vial_dialog(tag_selector, vial_serial) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4)
		{
			if (this.status == 200)
			{
				$(tag_selector + " > #message").innerHTML = this.responseText;
				$(tag_selector).dialog({
					resizable: false, 
					height: "auto", 
					width: 400, 
					modal: true, 
					buttons: {
						"Remove" : function() {
							// Remove vial from database
							$(this).dialog("close");
						}, 
						"Cancel": function() {
							$(this).dialog("close");
						}
					}
				});
			}
		}
	};
	var request_url = "showvial?serial=" + vial_serial;
	xhttp.open("GET", request_url, true);
	xhttp.send();
}
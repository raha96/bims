
function resolve_suffix(){
	suffixes = ["F", "C", "X"];
	suf_ids = ["suf1", "suf2", "suf3"];
	num = 3;
	//alert("CP");
	for (var i = 0; i < num; i++) {
		//alert(suf_ids[i]);
		//alert(suf_ids[i].checked == 1);
		//alert(document.getElementById(suf_ids[i]).checked);
		if (document.getElementById(suf_ids[i]).checked == 1) {
			return suffixes[i];
		}
	}
	return "X";
}

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
  request_url	 += "&passage_suffix=" + resolve_suffix();
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
  request_url	 += "&passage_suffix=" + resolve_suffix();
  xhttp.open("GET", request_url, true);
  document.getElementById(host_tag).innerHTML = "Querying codes...";
  xhttp.send();
}

function remove_request(vial_serial) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4)
		{
			if (this.status == 200)
			{
				fetch_visual_code("visual_code");
			}
		}
	};
	var request_url = "removevial?serial=" + vial_serial;
	xhttp.open("GET", request_url, true);
	xhttp.send();
}

function remove_vial_dialog(tag_selector, vial_serial) {
	var errorcnt = 1;
	var rmflag = false;
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4)
		{
			if (this.status == 200)
			{
				$(tag_selector).dialog({
					resizable: false, 
					height: "auto", 
					width: "auto", 
					modal: true, 
					buttons: {
						"Remove" : function() {
							// Remove vial from database
							remove_request(vial_serial);
							$(this).dialog("close");
						}, 
						"Cancel": function() {
							$(this).dialog("close");
						}
					}
				});
				jQuery("#message").html(xhttp.responseText);
			}
		}
	};
	var request_url = "showvial?serial=" + vial_serial;
	xhttp.open("GET", request_url, true);
	xhttp.send();
}

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
  request_url	 += "&passage=" + document.getElementById("passage").value;
  request_url	 += "&date_yy=" + document.getElementById("date_yy").value;
  request_url	 += "&date_mm=" + document.getElementById("date_mm").value;
  request_url	 += "&date_dd=" + document.getElementById("date_dd").value;
  request_url	 += "&location=" + document.getElementById("location").value;
  xhttp.open("GET", request_url, true);
  document.getElementById(host_tag).innerHTML = "Generating visual code...";
  xhttp.send();
}
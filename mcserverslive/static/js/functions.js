// text counter
function textCounter(field, cnt, maxlimit) {
	var remaining = maxlimit - field.value.length;
	if (field.value.length > maxlimit) {
		field.value = field.value.substring(0, maxlimit);
		document.getElementById(cnt).innerHTML = "characters left: 0";
	} else {
		document.getElementById(cnt).innerHTML = "characters left: " + remaining.toString();
	}
}

// remove duplicates from array
function ArrayUnique(arr) {
	var temp = {};
	for(var i=0; i<arr.length; i++)
		temp[arr[i]] = true;
	var uniq_arr = [];
	for(var j in temp)
		uniq_arr.push(j);
	return uniq_arr;
}

// update current info
function getCurrentData(data) {
	var variables = data.variables;
	var servers = data.data;
	var id = '';
	for(server in servers) {
		for(var i=0; i<variables.length; i++) {
			id = "#"+server+"__"+variables[i];
			if(variables[i] != 'banner') {
				$(id).html(servers[server][variables[i]]);
			} else {
				$(id).attr('src',servers[server][variables[i]]);
			}
		}
	}
}



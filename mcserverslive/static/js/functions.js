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

// flot
function Plot(flot_id, d, ymin, ymax) {

	var options = {

		series: {
			lines: { show: true, fill: true }
		},
		xaxis: { 
			mode: "time",
			twelveHourClock: true,
		},
		yaxis: {
			min: ymin,
			max: ymax
		}

	}
	var plot = $.plot(flot_id, [d], options);
	return plot
}

function makePlot(data) {
	
	var flot_id = data.flot_id;
	var ymax = $(data.ymax_id).html();
	var ymin = -1*(ymax/4);
	var data = data.data;	
	var d = [];

	for(var i in data){
		if(data[i] == null) data[i] = ymin;
		d.push([parseInt(i), data [i]]);
	}

	d.sort(function(a,b){return a[0]-b[0]});

	var plot = Plot(flot_id, d, ymin, ymax);
	plot.draw();
}

// voting
function voteSubmit() {
	Dajaxice.mcserverslive.vote(vote_result,{'user_pk': $('#user_pk').html(), 'pk': $('#pk').html() });
}
function vote_result(data) {
	$("#vote_message").html(data.data);
}



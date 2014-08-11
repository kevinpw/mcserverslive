function textCounter(field, cnt, maxlimit) {
	var remaining = maxlimit - field.value.length;
	if (field.value.length > maxlimit) {
		field.value = field.value.substring(0, maxlimit);
		document.getElementById(cnt).innerHTML = "characters left: 0";
	} else {
		document.getElementById(cnt).innerHTML = "characters left: " + remaining.toString();
	}
}

function updateText(data) {
	data = data.data
	$("#banner").attr( 'src',data['banner']);
	$("#version").html(data['version']);
	$("#game_type").html(data['game_type']);
	$("#max_players").html(data['max_players']);
	$("#num_players").html(data['numplayers']);
	$("#motd").html(data['motd']);
	$("#website").html(data['website']);
	$("#votes").html(data['votes']);
	$("#last_queried").html(data['last_queried']);
	$("#plugins").html(data['plugins']);
}

function Plot(flot_id, d, ymin, ymax) {

	var options = {

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

function vote_result(data) {
	$("#vote_message").html(data.data);
}



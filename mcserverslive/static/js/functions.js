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
//	$("#banner").attr('src'):{{ server.banner }}
	$("#version").html(data['version']);
	$("#game_type").html(data['game_type']);
	$("#max_players").html(data['max_players']);
	$("#num_players").html(data['numplayers']);
	$("#motd").html(data['motd']);
	$("#website").html(data['website']);
	$("#votes").html(data['votes']);
	$("#last_queried").html(data['last_queried']);
}

function plot(d, ymax) {
	$.plot("#flot_time_series", [d], {
		xaxis: { 
			mode: "time" 
		},
		yaxis: {
			min: 0,
			max: ymax
		}
	});
}	

function makePlot(data) {

	data = data.data;
	var d = [];

	for(var i in data){
		d.push([parseInt(i), data [i]]);
	}

	plot(d, $("#max_players").html());

}

function vote_result(data) {
	$("#vote_message").html(data.data);
}



function textCounter(field, cnt, maxlimit) {
	var remaining = maxlimit - field.value.length;
	if (field.value.length > maxlimit) {
		field.value = field.value.substring(0, maxlimit);
		document.getElementById(cnt).innerHTML = "characters left: 0";
	} else {
		document.getElementById(cnt).innerHTML = "characters left: " + remaining.toString();
	}
}

$(function() {

	function makePlot(data) {
		data = data.data;
		d = [];
		for(var i in data){
			d.push([parseInt(i), data [i]]);
		}
		
		console.log(d);
		$.plot("#flot_time_series", [d], {
			xaxis: { 
				mode: "time" 
			},
			yaxis: {
				min: 0,
				max: 100
			}
		});
	}		

	Dajaxice.mcserverslive.get_data(makePlot, {'pk': $("#pk").html() });

	setInterval( function() {
		Dajaxice.mcserverslive.get_data(makePlot, {'pk': $("#pk").html() })
		}, 20000 );
});

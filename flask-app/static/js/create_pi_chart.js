function create_pi_chart(subreddit_frequency_list, topic) {
    var subreddit_frequency_list = subreddit_frequency_list;
    var chart = {
	plotBackgroundColor: null,
	plotBorderWidth: null,
	plotShadow: false,
	renderTo: 'bar-graff'
    };
    var title = {
	text: 'What subreddits ' + topic + ' was mentioned in among your audience.'
    };
    var tooltip = {
	pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    };
    var plotOptions = {
	pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
		enabled: true,
		format: '<b>{point.name}%</b>: {point.percentage:.1f} %',
		style: {
		    color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
		}
            }
      }
    };
    // So need a function here to parse the json data.
    chart_data = [];
    for (var i = 0; i < subreddit_frequency_list.length; i++) {
	new_json = {};
	new_json.name = subreddit_frequency_list[i].text;
	new_json.y = subreddit_frequency_list[i].size;
	chart_data.push(new_json);
    }
    var series= [{
	type: 'pie',
	name: 'Subreddit share',
	data: chart_data
    }];
    
    var json = {};
    json.chart = chart;
    json.title = title;
    json.tooltip = tooltip;
    json.series = series;
    json.plotOptions = plotOptions;
    var chart = new Highcharts.Chart(json);   
}

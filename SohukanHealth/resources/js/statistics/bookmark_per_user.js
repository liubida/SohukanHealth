var make_bookmark_per_user_chart = function(chartData) {
	var e = document.getElementById('statistics_bookmark_per_user')
	clearElement(e);

	// SERIAL CHART
	var chart = new AmCharts.AmSerialChart();
	chart.dataProvider = chartData;
	chart.categoryField = "user_id";
	chart.startDuration = 1;
	chart.addTitle('用户收藏文章排行', 20);

	// AXES
	// category
	var categoryAxis = chart.categoryAxis;
	categoryAxis.labelRotation = 45; // this line makes category
	// values to be rotated
	categoryAxis.gridAlpha = 0;
	categoryAxis.fillAlpha = 1;
	categoryAxis.fillColor = "#FAFAFA";
	categoryAxis.gridPosition = "start";

	// value
	var valueAxis = new AmCharts.ValueAxis();
	valueAxis.dashLength = 5;
	valueAxis.title = "bookmark num"
	valueAxis.axisAlpha = 0;
	chart.addValueAxis(valueAxis);

	// GRAPH
	var graph = new AmCharts.AmGraph();
	graph.valueField = "count";
	graph.colorField = "color";
	graph.balloonText = "[[category]]: [[value]]";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	chart.addGraph(graph);

	// WRITE
	chart.write(e.getAttribute('id'));
};

var load_bookmark_per_user = function(params, callback) {
	url = '/statistics/bookmark/per_user';

	var from = $("#statistics_bookmark_per_user_from").val()
	var to = $("#statistics_bookmark_per_user_to").val()

	var date_range = get_date_range(from, to);
	var data_size = $("#table_bookmark_per_user #size").val();

	var params = {
		start_time : date_range.start_time,
		end_time : date_range.end_time,
		data_size : data_size
	};

	var e = document.getElementById('statistics_bookmark_per_user')
	clearElement(e);
	var loading = document.createElement('p')
	var loading_text = document.createTextNode('数据加载中...')
	loading.appendChild(loading_text);
	e.appendChild(loading);

	myAjax(url, params, function(obj) {
				data = obj.list;
				len = data.length;
				chartData = [];
				for (var i = 0; i < len; i++) {
					chartData.push({
								user_id : data[i].user_id,
								count : data[i].count,
								color : data[i].color
							});
				}
				make_bookmark_per_user_chart(chartData);
				if (callback && typeof callback == 'function') {
					callback();
				}
			});
};

var prepare_bookmark_per_user = function() {
	$("#statistics_bookmark_per_user_from").datepicker({
		changeMonth : true,
		numberOfMonths : 2,
		dateFormat : "yy-mm-dd"
			// ,
			// onSelect : function(selectedDate) {
			// $("#statistics_bookmark_per_user_to").datepicker("option",
			// "minDate", selectedDate);
			// }
		});
	$("#statistics_bookmark_per_user_to").datepicker({
				changeMonth : true,
				numberOfMonths : 2,
				dateFormat : "yy-mm-dd"
			});
	$("#table_bookmark_per_user #bookmark_per_user_submit")
			.click(load_bookmark_per_user);
	$("#table_bookmark_per_user #reset").click(function() {
				$("#statistics_bookmark_per_user_from").val('');
				$("#statistics_bookmark_per_user_to").val('');
			});

	load_bookmark_per_user();
};

$(document).ready(function() {
			prepare_bookmark_per_user();
		});
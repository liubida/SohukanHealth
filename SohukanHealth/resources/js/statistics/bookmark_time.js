var make_bookmark_time_chart = function(chartData, radio_type) {
	var e = document.getElementById('statistics_bookmark_time_div')
	clearElement(e);

	// SERIAL CHART
	var chart = new AmCharts.AmSerialChart();
	chart.dataProvider = chartData;
	chart.categoryField = "hour";
	chart.startDuration = 1;
	chart.addTitle('收藏文章时段统计', 20);

	// AXES
	// category
	var categoryAxis = chart.categoryAxis;
	categoryAxis.labelRotation = 45; // this line makes category
	// values to be rotated
	categoryAxis.gridAlpha = 0;
	categoryAxis.fillAlpha = 1;
	categoryAxis.fillColor = "#FAFAFA";
	categoryAxis.gridPosition = "start";

	// value1
	var valueAxis1 = new AmCharts.ValueAxis();
	valueAxis1.dashLength = 5;
	valueAxis1.title = "num"
	valueAxis1.axisAlpha = 0;
	chart.addValueAxis(valueAxis1);

	// value2
	var valueAxis2 = new AmCharts.ValueAxis();
	valueAxis2.position = "right";
	valueAxis2.axisColor = "#FCD202";
	valueAxis2.gridAlpha = 0;
	valueAxis2.axisThickness = 1;
	chart.addValueAxis(valueAxis2);

	// GRAPH
	var graph1 = new AmCharts.AmGraph();
	graph1.valueField = "count";
	graph1.colorField = "color";
	graph1.balloonText = "[[category]]: [[value]]";
	graph1.type = "column";
	graph1.lineAlpha = 0;
	graph1.fillAlphas = 1;
	chart.addGraph(graph1);

	// second graph
	var graph2 = new AmCharts.AmGraph();
	graph2.title = "yellow line";
	graph2.valueField = "percent";
	graph2.bullet = "round";
	graph2.valueAxis = valueAxis2;
	graph2.hideBulletsCount = 50;
	if (radio_type == 1) {
		chart.addGraph(graph2);
	}

	// WRITE
	chart.write(e.getAttribute('id'));
};

var load_bookmark_time = function(params, callback) {
	url = '/statistics/bookmark/time';

	var from = $("#statistics_bookmark_time_from").val()
	var to = $("#statistics_bookmark_time_to").val()
	var radio_type = parseInt($("#table_bookmark_time :radio:checked").val(),
			10);

	var date_range = get_date_range(from, to);
	params = {
		start_time : date_range.start_time,
		end_time : date_range.end_time
	};

	var e = document.getElementById('statistics_bookmark_time_div')
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
								hour : data[i].hour,
								count : data[i].count,
								color : data[i].color,
								percent : data[i].percent
							});
				}
				make_bookmark_time_chart(chartData, radio_type);
				prepare_bookmark_time.chartData = chartData;
				if (callback && typeof callback == 'function') {
					callback();
				}
			});
};
var prepare_bookmark_time = function() {
	$("#statistics_bookmark_time_from").datepicker({
		changeMonth : true,
		numberOfMonths : 2,
		dateFormat : "yy-mm-dd",
		onSelect : function(selectedDate) {
			$("#statistics_bookmark_time_to").datepicker("option", "minDate",
					selectedDate);
		}
	});
	$("#statistics_bookmark_time_to").datepicker({
				changeMonth : true,
				numberOfMonths : 2,
				dateFormat : "yy-mm-dd"
			});
	$("#table_bookmark_time :radio").change(function() {
		if (prepare_bookmark_time.chartData) {
			var radio_type = parseInt($("#table_bookmark_time :radio:checked")
							.val(), 10);
			make_bookmark_time_chart(prepare_bookmark_time.chartData,
					radio_type);
		} else {
			load_bookmark_time();
		}
	});
	$("#table_bookmark_time #submit").click(load_bookmark_time);
	$("#table_bookmark_time #reset").click(function() {
				$("#statistics_bookmark_time_from").val('');
				$("#statistics_bookmark_time_to").val('');
			});

	load_bookmark_time();
};

$(document).ready(function() {
			prepare_bookmark_time();
		});
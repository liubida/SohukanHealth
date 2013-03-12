var make_public_client_chart = function(chartData) {
	var e = document.getElementById('statistics_public_client');
	clearElement(e);

	chart = new AmCharts.AmSerialChart();
	chart.dataProvider = chartData;
	chart.categoryField = "time";

	// sometimes we need to set margins manually
	// autoMargins should be set to false in order chart to use custom
	// margin values
	chart.autoMargins = false;
	chart.marginLeft = 0;
	chart.marginRight = 0;
	chart.marginTop = 30;
	chart.marginBottom = 40;

	// AXES
	// category
	var categoryAxis = chart.categoryAxis;
	categoryAxis.gridAlpha = 0;
	categoryAxis.axisAlpha = 0;
	categoryAxis.gridPosition = "start";

	// value
	var valueAxis = new AmCharts.ValueAxis();
	valueAxis.stackType = "regular"; // this line makes the chart 100%
	// stacked
	valueAxis.gridAlpha = 0;
	valueAxis.axisAlpha = 0;
	valueAxis.labelsEnabled = false;
	chart.addValueAxis(valueAxis);

	// GRAPHS
	// first graph
	var graph = new AmCharts.AmGraph();
	graph.title = "iPhone";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.valueField = "iPhone";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#B0DE09";
	chart.addGraph(graph);

	// second graph
	var graph = new AmCharts.AmGraph();
	graph.title = "iPad";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.valueField = "iPad";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#FF9E01";
	chart.addGraph(graph);

	// third graph
	var graph = new AmCharts.AmGraph();
	graph.title = "android";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.valueField = "android";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#FCD202";
	chart.addGraph(graph);

	// 4th graph
	var graph = new AmCharts.AmGraph();
	graph.title = "unknown";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.valueField = "unknown";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#0D8ECF";
	chart.addGraph(graph);

	// LEGEND
	var legend = new AmCharts.AmLegend();
	legend.borderAlpha = 0.2;
	legend.horizontalGap = 10;
	legend.autoMargins = false;
	legend.marginLeft = 20;
	legend.marginRight = 20;
	legend.switchType = "v";
	chart.addLegend(legend);

	// WRITE
	chart.write(e.getAttribute('id'));
};

var load_public_client = function(params, callback) {
	url = '/statistics/bookmark/public_client';

	var now = new Date();
	var to = $("#statistics_public_client_to").val()
	to = to || now.format('yyyy-MM-dd hh:mm:ss');
	var from = $("#statistics_public_client_from").val()
	tmp = now;
	tmp.setMonth(2);
	tmp.setDate(12);
	tmp.setYear(2013);
	from = from || tmp.format('yyyy-MM-dd hh:mm:ss');

	var date_range = get_date_range(from, to);
	var data_grain = $("#table_public_client #data_grain").val();
	// var radio_type = parseInt($("#table_activate_user :radio:checked").val(),
	// 10);

	var params = {
		start_time : date_range.start_time,
		end_time : date_range.end_time,
		data_grain : data_grain
	};

	var e = document.getElementById('statistics_public_client')
	clearElement(e);
	var loading = document.createElement('p')
	var loading_text = document.createTextNode('数据加载中...')
	loading.appendChild(loading_text);
	e.appendChild(loading);

	myAjax(url, params, function(obj) {
				data = obj;
				len = data.length;
				chartData = [];
				for (var i = 0; i < len; i++) {
					chartData.push({
								iPhone : data[i].iPhone,
								iPad : data[i].iPad,
								android : data[i].android,
                                unknown: data[i].unknown
							});
				}
				make_public_client_chart(chartData);
				prepare_public_client.chartData = chartData;
				if (callback && typeof callback == 'function') {
					callback();
				}
				$("#statistics_public_client_from").val(from.substr(0, 10));
				$("#statistics_public_client_to").val(to.substr(0, 10));
			});
};
var prepare_public_client = function() {
	$("#statistics_public_client_from").datepicker({
		changeMonth : true,
		numberOfMonths : 2,
		dateFormat : "yy-mm-dd"
			// ,
			// onSelect : function(selectedDate) {
			// $("#statistics_public_client_to").datepicker("option",
			// "minDate",
			// selectedDate);
			// }
		});
	$("#statistics_public_client_to").datepicker({
				changeMonth : true,
				numberOfMonths : 2,
				dateFormat : "yy-mm-dd"
			});
	$("#table_public_client #data_grain").change(load_public_client);
	$("#public_client_submit").click(load_public_client);
	$("#table_public_client #reset").click(function() {
				$("#statistics_public_client_from").val('');
				$("#statistics_public_client_to").val('');
			});

	load_public_client();
};

$(document).ready(function() {
			prepare_public_client();
		});

var make_add_channels_chart = function(chartData) {
	var e = document.getElementById('statistics_add_channels');
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
	graph.title = "share";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.valueField = "share";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#B0DE09";
	chart.addGraph(graph);

	// second graph
	var graph = new AmCharts.AmGraph();
	graph.title = "chrome";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.valueField = "chrome";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#FF9E01";
	chart.addGraph(graph);

	// third graph
	var graph = new AmCharts.AmGraph();
	graph.title = "sogou";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.valueField = "sogou";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#FCD202";
	chart.addGraph(graph);

	// 4th graph
	var graph = new AmCharts.AmGraph();
	graph.title = "iPhone";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.valueField = "iPhone";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#0d8ecf";
	chart.addGraph(graph);
    
	// 5th graph
	var graph = new AmCharts.AmGraph();
	graph.title = "iPad";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.valueField = "iPad";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#04d215";
	chart.addGraph(graph);

	// 6th graph
	var graph = new AmCharts.AmGraph();
	graph.title = "android";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.valueField = "android";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#CD0D74";
	chart.addGraph(graph);

	// 7th graph
	var graph = new AmCharts.AmGraph();
	graph.title = "other";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.valueField = "other";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#DAF0FD";
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

var load_add_channels = function(params, callback) {
	url = '/statistics/bookmark/add_channels';

	var now = new Date();
	var to = $("#statistics_add_channels_to").val()
	to = to || now.format('yyyy-MM-dd hh:mm:ss');
	var from = $("#statistics_add_channels_from").val()
	tmp = now;
	tmp.setMonth(3);
	tmp.setDate(1);
	tmp.setYear(2013);
	from = from || tmp.format('yyyy-MM-dd hh:mm:ss');

	var date_range = get_date_range(from, to);
	var data_grain = $("#table_add_channels #data_grain").val();
	// var radio_type = parseInt($("#table_activate_user :radio:checked").val(),
	// 10);

	var params = {
		start_time : date_range.start_time,
		end_time : date_range.end_time,
		data_grain : data_grain
	};

	var e = document.getElementById('statistics_add_channels')
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
								time : data[i].time,
								share : data[i].share,
								sogou : data[i].sogou,
								chrome : data[i].chrome,
                                iPhone : data[i].iPhone,
                                iPad : data[i].iPad,
                                android : data[i].android,
								other : data[i].other
							});
				}
				make_add_channels_chart(chartData);
				prepare_add_channel.chartData = chartData;
				if (callback && typeof callback == 'function') {
					callback();
				}
				$("#statistics_add_channels_from").val(from.substr(0, 10));
				$("#statistics_add_channels_to").val(to.substr(0, 10));
			});
};
var prepare_add_channel = function() {
	$("#statistics_add_channels_from").datepicker({
		changeMonth : true,
		numberOfMonths : 2,
		dateFormat : "yy-mm-dd"
			// ,
			// onSelect : function(selectedDate) {
			// $("#statistics_add_channels_to").datepicker("option",
			// "minDate",
			// selectedDate);
			// }
		});
	$("#statistics_add_channels_to").datepicker({
				changeMonth : true,
				numberOfMonths : 2,
				dateFormat : "yy-mm-dd"
			});
	$("#table_add_channels #data_grain").change(load_add_channels);
	$("#add_channels_submit").click(load_add_channels);
	$("#table_add_channels #reset").click(function() {
				$("#statistics_add_channels_from").val('');
				$("#statistics_add_channels_to").val('');
			});

	load_add_channels();
};

$(document).ready(function() {
			prepare_add_channel();
		});

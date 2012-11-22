var make_share_channels_chart = function(chartData) {
	var e = document.getElementById('statistics_share_channels');
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
	graph.title = "bshare";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.valueField = "bshare";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#B0DE09";
	chart.addGraph(graph);

	// second graph
	var graph = new AmCharts.AmGraph();
	graph.title = "jiathis";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.valueField = "jiathis";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#FF9E01";
	chart.addGraph(graph);

	// third graph
	var graph = new AmCharts.AmGraph();
	graph.title = "webapp";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.valueField = "webapp";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#FCD202";
	chart.addGraph(graph);

	// 4th graph
	var graph = new AmCharts.AmGraph();
	graph.title = "sohu_blog";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.valueField = "sohu_blog";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#0d8ecf";
	chart.addGraph(graph);
    
	// 5th graph
	var graph = new AmCharts.AmGraph();
	graph.title = "sohu_news";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.valueField = "sohu_news";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#04d215";
	chart.addGraph(graph);

	// 6th graph
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

var load_share_channels = function(params, callback) {
	url = '/statistics/bookmark/share_channels';

	var now = new Date();
	var to = $("#statistics_share_channels_to").val()
	to = to || now.format('yyyy-MM-dd hh:mm:ss');
	var from = $("#statistics_share_channels_from").val()
	tmp = now;
	tmp.setMonth(9);
	tmp.setDate(24);
	tmp.setYear(2012);
	from = from || tmp.format('yyyy-MM-dd hh:mm:ss');

	var date_range = get_date_range(from, to);
	var data_grain = $("#table_share_channels #data_grain").val();
	// var radio_type = parseInt($("#table_activate_user :radio:checked").val(),
	// 10);

	var params = {
		start_time : date_range.start_time,
		end_time : date_range.end_time,
		data_grain : data_grain
	};

	var e = document.getElementById('statistics_share_channels')
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
								bshare : data[i].bshare,
								jiathis : data[i].jiathis,
								webapp : data[i].webapp,
                                sohu_blog : data[i].sohu_blog,
                                sohu_news : data[i].sohu_news,
								other : data[i].share
							});
				}
				make_share_channels_chart(chartData);
				prepare_share_channel.chartData = chartData;
				if (callback && typeof callback == 'function') {
					callback();
				}
				$("#statistics_share_channels_from").val(from.substr(0, 10));
				$("#statistics_share_channels_to").val(to.substr(0, 10));
			});
};
var prepare_share_channel = function() {
	$("#statistics_share_channels_from").datepicker({
		changeMonth : true,
		numberOfMonths : 2,
		dateFormat : "yy-mm-dd"
			// ,
			// onSelect : function(selectedDate) {
			// $("#statistics_share_channels_to").datepicker("option",
			// "minDate",
			// selectedDate);
			// }
		});
	$("#statistics_share_channels_to").datepicker({
				changeMonth : true,
				numberOfMonths : 2,
				dateFormat : "yy-mm-dd"
			});
	$("#table_share_channels #data_grain").change(load_share_channels);
	$("#share_channels_submit").click(load_share_channels);
	$("#table_share_channels #reset").click(function() {
				$("#statistics_share_channels_from").val('');
				$("#statistics_share_channels_to").val('');
			});

	load_share_channels();
};

$(document).ready(function() {
			prepare_share_channel();
		});

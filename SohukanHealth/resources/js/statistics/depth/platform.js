var make_platform_chart = function(chartData) {
	var e = document.getElementById('depth_platform')
	clearElement(e);

	chart = new AmCharts.AmSerialChart();
	chart.zoomOutButton = {
		backgroundColor : "#000000",
		backgroundAlpha : 0.15
	};
	chart.dataProvider = chartData;
	chart.categoryField = "time";
	chart.addTitle("活跃用户使用平台", 20);

	var categoryAxis = chart.categoryAxis;
	categoryAxis.gridAlpha = 0.07;
	categoryAxis.axisColor = "#DADADA";
	categoryAxis.startOnAxis = true;

	// Value
	var valueAxis = new AmCharts.ValueAxis();
	valueAxis.title = "percent"; // this line makes the chart "stacked"
	valueAxis.stackType = "100%";
	valueAxis.gridAlpha = 0.07;
	chart.addValueAxis(valueAxis);

	var graph = new AmCharts.AmGraph();
	graph.type = "line"; // it's simple line graph
	graph.title = "Android 手机用户";
	graph.valueField = "Android";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.lineAlpha = 0;
	graph.fillAlphas = 0.6; // setting fillAlphas to > 0 value makes it area
	// graph
	chart.addGraph(graph);

	var graph = new AmCharts.AmGraph();
	graph.type = "line";
	graph.title = "IOS 手机用户";
	graph.valueField = "Darwin";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.lineAlpha = 0;
	graph.fillAlphas = 0.6;
	chart.addGraph(graph);

	// fourth graph
	var graph = new AmCharts.AmGraph();
	graph.type = "line";
	graph.title = "Windows 平台PC";
	graph.valueField = "Windows";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.lineAlpha = 0;
	graph.fillAlphas = 0.6;
	chart.addGraph(graph);

	// third graph
	var graph = new AmCharts.AmGraph();
	graph.type = "line";
	graph.title = "Mac 平台PC";
	graph.valueField = "Macintosh";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.lineAlpha = 0;
	graph.fillAlphas = 0.6;
	chart.addGraph(graph);

	// fifth graph
	var graph = new AmCharts.AmGraph();
	graph.type = "line";
	graph.title = "Linux  平台PC";
	graph.valueField = "Linux";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.lineAlpha = 0;
	graph.fillAlphas = 0.6;
	chart.addGraph(graph);

	// fifth graph
	var graph = new AmCharts.AmGraph();
	graph.type = "line";
	graph.title = "unknown";
	graph.valueField = "unknown";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.lineAlpha = 0;
	graph.fillAlphas = 0.6;
	chart.addGraph(graph);

	// LEGEND
	var legend = new AmCharts.AmLegend();
	legend.align = "center";
	chart.addLegend(legend);

	// CURSOR
	var chartCursor = new AmCharts.ChartCursor();
	chartCursor.zoomable = false; // as the chart displayes not too many
	// values, we disabled zooming
	chartCursor.cursorAlpha = 0;
	chart.addChartCursor(chartCursor);

	chart.write(e.getAttribute('id'));
};

var load_platform = function(params, callback) {
	url = '/statistics/depth/platform';

	var from = $("#depth_platform_from").val()
	var to = $("#depth_platform_to").val()

	var date_range = get_date_range(from, to);
	var size = $("#table_platform #size").val();

	var params = {
		start_time : date_range.start_time,
		end_time : date_range.end_time,
		size : size
	};

	var e = document.getElementById('depth_platform')
	clearElement(e);
	var loading = document.createElement('p')
	var loading_text = document.createTextNode('数据加载中...')
	loading.appendChild(loading_text);
	e.appendChild(loading);

	myAjax(url, params, function(obj) {
				data = obj.list;
				len = data.length;

				make_platform_chart(data);
				prepare_platform.data = data;

				if (callback && typeof callback == 'function') {
					callback();
				}
			});
};

var prepare_platform = function() {
	$("#depth_platform_from").datepicker({
		changeMonth : true,
		numberOfMonths : 2,
		dateFormat : "yy-mm-dd",
		onSelect : function(selectedDate) {
			$("#depth_platform_to").datepicker("option", "minDate",
					selectedDate);
		}
	});
	$("#depth_platform_to").datepicker({
				changeMonth : true,
				numberOfMonths : 2,
				dateFormat : "yy-mm-dd"
			});
	$("#table_platform #submit").click(load_platform);
	$("#table_platform #reset").click(function() {
				$("#depth_platform_from").val('');
				$("#depth_platform_to").val('');
			});

	load_platform();
};

$(document).ready(function() {
			prepare_platform();
		});
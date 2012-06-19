var chart;
var chartData = [];
var chartCursor;

AmCharts.ready(function() {
	add_div();
	read_div();
});

function add_div() {
	// generate some data first
//	var avg_visits = 
	get_chart_data('add');

	// SERIAL CHART
	chart = new AmCharts.AmSerialChart();
	chart.pathToImages = "/static/images/";
	chart.zoomOutButton = {
		backgroundColor : '#000000',
		backgroundAlpha : 0.15
	};
	chart.dataProvider = chartData;
	chart.categoryField = "date";

	// listen for "dataUpdated" event (fired when chart is rendered) and call
	// zoomChart method when it happens
	chart.addListener("dataUpdated", function() {
		// different zoom methods can be used - zoomToIndexes, zoomToDates,
		// zoomToCategoryValues
		chart.zoomToIndexes(chartData.length - 8, chartData.length - 1);
	});
	
	// AXES
	// category
	var categoryAxis = chart.categoryAxis;
	// categoryAxis.parseDates = true; // as our data is date-based, we set
	// parseDates to true
	categoryAxis.minPeriod = "ss"; // our data is daily, so we set minPeriod to
	// DD
	categoryAxis.dashLength = 1;
	categoryAxis.gridAlpha = 0.15;
	categoryAxis.axisColor = "#DADADA";
	// categoryAxis.labelsEnabled=false;
	categoryAxis.labelFrequency = 0.1;

	// value
	var valueAxis = new AmCharts.ValueAxis();
	valueAxis.axisAlpha = 0.2;
	valueAxis.dashLength = 1;
	chart.addValueAxis(valueAxis);

	// GRAPH
	var graph = new AmCharts.AmGraph();
	graph.title = "red line";
	graph.valueField = "time_used";
	graph.bullet = "round";
	graph.bulletBorderColor = "#FFFFFF";
	graph.bulletBorderThickness = 2;
	graph.lineThickness = 2;
	graph.lineColor = "#b5030d";
	graph.negativeLineColor = "#0352b5";
	graph.hideBulletsCount = 50; // this makes the chart to hide bullets when
	// there are more than 50 series in
	// selection
	graph.negativeBase = 0
	chart.addGraph(graph);

	// CURSOR
	chartCursor = new AmCharts.ChartCursor();
	chartCursor.cursorPosition = "mouse";
	chart.addChartCursor(chartCursor);

	// SCROLLBAR
	var chartScrollbar = new AmCharts.ChartScrollbar();
	chartScrollbar.graph = graph;
	chartScrollbar.scrollbarHeight = 40;
	chartScrollbar.color = "#FFFFFF";
	chartScrollbar.autoGridCount = true;
	chart.addChartScrollbar(chartScrollbar);

	// WRITE
	chart.write("add_div");
};

function read_div() {
	// generate some data first
	get_chart_data('read');

	// SERIAL CHART
	chart = new AmCharts.AmSerialChart();
	// chart.pathToImages = "../amcharts/images/";
	chart.pathToImages = "/static/images/";
	chart.zoomOutButton = {
		backgroundColor : '#000000',
		backgroundAlpha : 0.15
	};
	chart.dataProvider = chartData;
	chart.categoryField = "date";

	// listen for "dataUpdated" event (fired when chart is rendered) and call
	// zoomChart method when it happens
	chart.addListener("dataUpdated", function() {
		// different zoom methods can be used - zoomToIndexes, zoomToDates,
		// zoomToCategoryValues
		chart.zoomToIndexes(chartData.length - 9, chartData.length - 1);
	});

	// AXES
	// category
	var categoryAxis = chart.categoryAxis;
	// categoryAxis.parseDates = true; // as our data is date-based, we set
	// parseDates to true
	categoryAxis.minPeriod = "ss"; // our data is daily, so we set minPeriod to
	// DD
	categoryAxis.dashLength = 1;
	categoryAxis.gridAlpha = 0.15;
	categoryAxis.axisColor = "#DADADA";
	// categoryAxis.labelsEnabled=false;
	categoryAxis.labelFrequency = 0.1;

	// value
	var valueAxis = new AmCharts.ValueAxis();
	valueAxis.axisAlpha = 0.2;
	valueAxis.dashLength = 1;
	chart.addValueAxis(valueAxis);

	// GRAPH
	var graph = new AmCharts.AmGraph();
	graph.title = "red line";
	graph.valueField = "time_used";
	graph.bullet = "round";
	graph.bulletBorderColor = "#FFFFFF";
	graph.bulletBorderThickness = 2;
	graph.lineThickness = 2;
	graph.lineColor = "#b5030d";
	graph.negativeLineColor = "#0352b5";
	graph.hideBulletsCount = 50; // this makes the chart to hide bullets when
	// there are more than 50 series in
	// selection
	graph.negativeBase = 0;
	chart.addGraph(graph);

	// CURSOR
	chartCursor = new AmCharts.ChartCursor();
	chartCursor.cursorPosition = "mouse";
	chart.addChartCursor(chartCursor);

	// SCROLLBAR
	var chartScrollbar = new AmCharts.ChartScrollbar();
	chartScrollbar.graph = graph;
	chartScrollbar.scrollbarHeight = 40;
	chartScrollbar.color = "#FFFFFF";
	chartScrollbar.autoGridCount = true;
	chart.addChartScrollbar(chartScrollbar);

	// WRITE
	chart.write("read_div");
};

var get_chart_data = function(name) {
	data = get_monitor_data(name)
	len = data.length;
	chartData = [];
	for ( var i = 0; i < len; i++) {
		chartData.push({
			date : data[i].time,
			time_used : data[i].time_used
		});
	}
}

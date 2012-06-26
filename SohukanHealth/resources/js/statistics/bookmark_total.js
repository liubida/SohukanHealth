var make_bookmark_total_chart = function(chartData) {
	var e = document.getElementById('bookmark_total_div')
	clearElement(e);
	
	// SERIAL CHART
	var chart = new AmCharts.AmSerialChart();
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
				// different zoom methods can be used - zoomToIndexes,
				// zoomToDates,
				// zoomToCategoryValues
				chart
						.zoomToIndexes(chartData.length - 48, chartData.length
										- 1);
			});
	chart.addTitle('添加文章数', 20);

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
	graph.valueField = "count";
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
	var chartCursor = new AmCharts.ChartCursor();
	chartCursor.cursorPosition = "mouse";
	chartCursor.pan = true;
	chart.addChartCursor(chartCursor);

	// SCROLLBAR
	var chartScrollbar = new AmCharts.ChartScrollbar();
	chartScrollbar.graph = graph;
	chartScrollbar.scrollbarHeight = 40;
	chartScrollbar.color = "#FFFFFF";
	chartScrollbar.autoGridCount = true;
	chart.addChartScrollbar(chartScrollbar);

	// WRITE
	chart.write("bookmark_total_div");
};

var load_bookmark_total = function(params, callback) {
	url = '/statistics/bookmark/total'

	myAjax(url, params, function(obj) {
				if (callback && typeof callback == 'function') {
					callback();
				}
				data = obj.list;
				len = data.length;
				chartData = [];
				for (var i = 0; i < len; i++) {
					chartData.push({
								date : chart_date_handler(data[i].time),
								count : data[i].count
							});
				}
				make_bookmark_total_chart(chartData);
			});
};

AmCharts.ready(function() {
			load_bookmark_total(null, null);
		});
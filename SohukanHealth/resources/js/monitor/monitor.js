var make_add_chart = function(chartData) {
	var e = document.getElementById('add_div')
	clearElement(e);

	var avg = get_avg_time_used(chartData);

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
				chart.zoomToIndexes(chartData.length - 100, chartData.length
								- 1);
			});
	chart.addTitle('添加文章所需时间', 20);

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

	// GUIDE for average
	var guide = new AmCharts.Guide();
	guide.value = avg;
	guide.lineColor = "#CC0000";
	guide.dashLength = 4;
	guide.label = "average";
	guide.inside = true;
	guide.lineAlpha = 1;
	valueAxis.addGuide(guide);

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
	graph.negativeBase = avg;
	chart.addGraph(graph);

	// CURSOR
	var chartCursor = new AmCharts.ChartCursor();
	chartCursor.cursorPosition = "mouse";
	chart.addChartCursor(chartCursor);

	// SCROLLBAR
	var chartScrollbar = new AmCharts.ChartScrollbar();
	chartScrollbar.graph = graph;
	chartScrollbar.scrollbarHeight = 40;
	chartScrollbar.color = "#FFFFFF";
	chartScrollbar.autoGridCount = false;
	chart.addChartScrollbar(chartScrollbar);

	// WRITE
	chart.write("add_div");
};

var make_read_chart = function(chartData) {
	var e = document.getElementById('read_div')
	clearElement(e);
	var avg = get_avg_time_used(chartData);

	// SERIAL CHART
	var chart = new AmCharts.AmSerialChart();
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
				// different zoom methods can be used - zoomToIndexes,
				// zoomToDates,
				// zoomToCategoryValues
				chart.zoomToIndexes(chartData.length - 100, chartData.length
								- 1);
			});
	chart.addTitle('阅读文章所需时间', 20);

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

	// GUIDE for average
	var guide = new AmCharts.Guide();
	guide.value = avg;
	guide.lineColor = "#CC0000";
	guide.dashLength = 4;
	guide.label = "average";
	guide.inside = true;
	guide.lineAlpha = 1;
	valueAxis.addGuide(guide);

	// GRAPH
	var graph = new AmCharts.AmGraph();
	graph.title = "red line";
	graph.valueField = "time_used";
	graph.bullet = "round";
	graph.bulletBorderColor = "#FFFFFF";
	graph.bulletBorderThickness = 4;
	graph.lineThickness = 2;
	graph.lineColor = "#b5030d";
	graph.negativeLineColor = "#0352b5";
	graph.hideBulletsCount = 50; // this makes the chart to hide bullets when
	// there are more than 50 series in
	// selection
	graph.negativeBase = avg;
	chart.addGraph(graph);

	// CURSOR
	var chartCursor = new AmCharts.ChartCursor();
	chartCursor.cursorPosition = "mouse";
	chart.addChartCursor(chartCursor);

	// SCROLLBAR
	var chartScrollbar = new AmCharts.ChartScrollbar();
	chartScrollbar.graph = graph;
	chartScrollbar.scrollbarHeight = 40;
	chartScrollbar.color = "#FFFFFF";
	chartScrollbar.autoGridCount = false;
	chart.addChartScrollbar(chartScrollbar);

	// WRITE
	chart.write("read_div");
};

var load_chart_data = function(name, params, callback) {
	var e = null;
	var url = null;
	if (name == 'read') {
		url = '/monitor/read'
		e = document.getElementById('read_div')
	}
	if (name == 'add') {
		url = '/monitor/add'
		e = document.getElementById('add_div')
	}

	if (e) {
		clearElement(e);

		var loading = document.createElement('p')
		var loading_text = document.createTextNode('数据加载中...')
		loading.appendChild(loading_text);
		e.appendChild(loading);
	}

	myAjax(url, params, function(obj) {
				data = obj.list;
				len = data.length;
				chartData = [];
				for (var i = 0; i < len; i++) {
					chartData.push({
								date : chart_date_handler(data[i].time),
								time_used : data[i].time_used
							});
				}
				if (name == 'read') {
					make_read_chart(chartData);
				}
				if (name == 'add') {
					make_add_chart(chartData);
				}

				if (callback && typeof callback == 'function') {
					callback();
				}
			});
};

var load_sys_alarm = function(params, callback) {
	var url = '/monitor/sys_alarm'
	var e = document.getElementById('sys_alarm')

	if (e) {
		clearElement(e);

		var loading = document.createElement('p')
		var loading_text = document.createTextNode('数据加载中...')
		loading.appendChild(loading_text);
		e.appendChild(loading);
	}
	url = url + '/' + params + '/'
	$('#sys_alarm').load(url);
};

var get_avg_time_used = function(chartData) {
	if (!chartData)
		return 0;

	var avg = 0, sum = 0;
	var len = chartData.length;
	for (var i = 0; i < len; i++) {
		sum += chartData[i].time_used;
	}
	return sum / len;
};
var prepare_monitor = function() {
	$('#app_available tr').mouseover(function() {
				// this.style.fontWeight = 'bold';
				this.style.backgroundColor = '#DFF7F8';
			});
	$('#app_available tr').mouseout(function() {
				this.style.backgroundColor = 'white';
			});
	$('#app_available tr').click(function() {
				load_sys_alarm(this.id.split('_')[2]);
			});
};
AmCharts.ready(function() {
			prepare_monitor();
			load_chart_data('read');
			load_chart_data('add');
		});
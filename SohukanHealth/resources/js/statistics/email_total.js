var make_email_total_chart = function(chartData, radio_type) {
	var e = document.getElementById('statistics_email_total')
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

	if (chartData.length > 100) {
		chart.addListener("dataUpdated", function() {
					chart.zoomToIndexes(chartData.length - 100,
							chartData.length - 1);
				});
	}
	chart.addTitle('通过邮件添加文章数', 20);

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

	// value1
	var valueAxis1 = new AmCharts.ValueAxis();
	valueAxis1.axisAlpha = 0.2;
	valueAxis1.dashLength = 1;
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
	graph1.valueAxis = valueAxis1;
	graph1.title = "red line";
	graph1.valueField = "count";
	graph1.bullet = "round";
	graph1.bulletBorderColor = "#FFFFFF";
	graph1.bulletBorderThickness = 2;
	graph1.lineThickness = 3;
	graph1.lineColor = "#b5030d";
	graph1.negativeLineColor = "#0352b5";
	graph1.hideBulletsCount = 50;
	graph1.negativeBase = 0
	chart.addGraph(graph1);

	// second graph
	var graph2 = new AmCharts.AmGraph();
	graph2.title = "yellow line";
	graph2.valueField = "inc";
	graph2.bullet = "round";
	graph2.valueAxis = valueAxis2;
	graph2.hideBulletsCount = 50;
	if (radio_type == 1) {
		chart.addGraph(graph2);
	}

	// CURSOR
	var chartCursor = new AmCharts.ChartCursor();
	chartCursor.cursorPosition = "mouse";
	chartCursor.pan = true;
	chart.addChartCursor(chartCursor);

	// SCROLLBAR
	var chartScrollbar = new AmCharts.ChartScrollbar();
	chartScrollbar.graph = graph1;
	chartScrollbar.scrollbarHeight = 40;
	chartScrollbar.color = "#FFFFFF";
	chartScrollbar.autoGridCount = true;
	chart.addChartScrollbar(chartScrollbar);

	// WRITE
	chart.write(e.getAttribute('id'));
};

var load_email_total = function(params, callback) {
	url = '/statistics/bookmark/email/'

	var now = new Date();
	var to = $("#statistics_email_total_to").val()
	to = to || now.format('yyyy-MM-dd hh:mm:ss');
	var from = $("#statistics_email_total_from").val()
	tmp = now;
	tmp.setMonth(2);
	tmp.setDate(13);
	tmp.setYear(2013);
	from = from || tmp.format('yyyy-MM-dd hh:mm:ss');

	var date_range = get_date_range(from, to);
	var data_grain = $("#table_email_total #data_grain").val();
	var radio_type = parseInt($("#table_email_total :radio:checked").val(),
			10);

	params = {
		start_time : date_range.start_time,
		end_time : date_range.end_time,
		data_grain : data_grain
	};

	var e = document.getElementById('statistics_email_total');
	clearElement(e);
	var loading = document.createElement('p')
	var loading_text = document.createTextNode('数据加载中...')
	loading.appendChild(loading_text);
	e.appendChild(loading);

	myAjax(url, params, function(obj) {
				if (callback && typeof callback == 'function') {
					callback();
				}
				data = obj.list;
				len = data.length;
				chartData = [];
				for (var i = 0; i < len; i++) {
					chartData.push({
								date : data[i].time,
								count : data[i].count,
								inc : data[i].inc
							});
				}
				make_email_total_chart(chartData, radio_type);
				prepare_email_total.chartData = chartData;
				$("#statistics_email_total_from").val(from.substr(0, 10));
				$("#statistics_email_total_to").val(to.substr(0, 10));
			});
};

var prepare_email_total = function() {
	$("#statistics_email_total_from").datepicker({
		changeMonth : true,
		numberOfMonths : 2,
		dateFormat : "yy-mm-dd"
			// ,
			// onSelect : function(selectedDate) {
			// $("#statistics_email_total_to").datepicker("option",
			// "minDate",
			// selectedDate);
			// }
		});
	$("#statistics_email_total_to").datepicker({
				changeMonth : true,
				numberOfMonths : 2,
				dateFormat : "yy-mm-dd"
			});
	$("#table_email_total #data_grain").change(load_email_total);
	$("#table_email_total :radio").change(function() {

		if (prepare_email_total.chartData) {
			var radio_type = parseInt($("#table_email_total :radio:checked")
							.val(), 10);
			make_email_total_chart(prepare_email_total.chartData,
					radio_type);
		} else {
			load_email_total();
		}
	});
	$("#table_email_total #email_total_submit")
			.click(load_email_total);
	$("#table_email_total #reset").click(function() {
				$("#statistics_email_total_from").val('');
				$("#statistics_email_total_to").val('');
			});
	load_email_total();
};
$(document).ready(function() {
			prepare_email_total();
		});

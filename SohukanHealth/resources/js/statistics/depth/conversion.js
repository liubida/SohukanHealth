var make_conversion_chart = function(chartData) {
	var e = document.getElementById('depth_conversion');
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
	graph.title = "plug-in";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[percents]]%)";
	graph.valueField = "plug_in";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#FF9E01";
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

var load_conversion = function(params, callback) {
	url = '/statistics/depth/conversion/';

	var now = new Date();
	var to = $("#depth_conversion_to").val()
	to = to || now.format('yyyy-MM-dd hh:mm:ss');
	var from = $("#depth_conversion_from").val()
	tmp = now;
	tmp.setMonth(2);
	tmp.setDate(12);
	tmp.setYear(2013);
	from = from || tmp.format('yyyy-MM-dd hh:mm:ss');

	var date_range = get_date_range(from, to);
	var data_grain = $("#table_conversion #data_grain").val();
	// var radio_type = parseInt($("#table_activate_user :radio:checked").val(),
	// 10);

	var params = {
		start_time : date_range.start_time,
		end_time : date_range.end_time,
		data_grain : data_grain
	};

	var e = document.getElementById('depth_conversion')
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
								plug_in : data[i].plug_in
							});
				}
				make_conversion_chart(chartData);
				prepare_conversion.chartData = chartData;
				if (callback && typeof callback == 'function') {
					callback();
				}
				$("#depth_conversion_from").val(from.substr(0, 10));
				$("#depth_conversion_to").val(to.substr(0, 10));
			});
};
var prepare_conversion = function() {
	$("#depth_conversion_from").datepicker({
		changeMonth : true,
		numberOfMonths : 2,
		dateFormat : "yy-mm-dd"
			// ,
			// onSelect : function(selectedDate) {
			// $("#depth_conversion_to").datepicker("option",
			// "minDate",
			// selectedDate);
			// }
		});
	$("#depth_conversion_to").datepicker({
				changeMonth : true,
				numberOfMonths : 2,
				dateFormat : "yy-mm-dd"
			});
	$("#table_conversion #data_grain").change(load_conversion);
	$("#conversion_submit").click(load_conversion);
	$("#table_conversion #reset").click(function() {
				$("#depth_conversion_from").val('');
				$("#depth_conversion_to").val('');
			});

	load_conversion();
};

$(document).ready(function() {
			prepare_conversion();
		});

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
	graph.title = "share_to_phone";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[title]])";
	graph.valueField = "share_to_phone";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#CC6699";
	chart.addGraph(graph);

	// second graph
	var graph = new AmCharts.AmGraph();
	graph.title = "share_to_pad";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[title]])";
	graph.valueField = "share_to_pad";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#FF6699";
	chart.addGraph(graph);

	// third graph
	var graph = new AmCharts.AmGraph();
	graph.title = "share_to_pc";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[title]])";
	graph.valueField = "share_to_pc";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#993366";
	chart.addGraph(graph);

	// 4th graph
	var graph = new AmCharts.AmGraph();
	graph.title = "share_to_unknown";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[title]])";
	graph.valueField = "share_to_unknown";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#CC0066";
	chart.addGraph(graph);
    
	// 5th graph
	var graph = new AmCharts.AmGraph();
	graph.title = "plug_in_to_phone";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[title]])";
	graph.valueField = "plug_in_to_phone";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#660099";
	chart.addGraph(graph);

	// 6th graph
	var graph = new AmCharts.AmGraph();
	graph.title = "plug_in_to_pad";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[title]])";
	graph.valueField = "plug_in_pad";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#9933CC";
	chart.addGraph(graph);

	// 7th graph
	var graph = new AmCharts.AmGraph();
	graph.title = "plug_in_to_pc";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[title]])";
	graph.valueField = "plug_in_to_pc";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#0066CC";
	chart.addGraph(graph);
    
	// 8th graph
	var graph = new AmCharts.AmGraph();
	graph.title = "plug_in_to_unknown";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[title]])";
	graph.valueField = "plug_in_to_unknown";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#33CCFF";
	chart.addGraph(graph);
    
	// 9th graph
	var graph = new AmCharts.AmGraph();
	graph.title = "mobile_phone";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[title]])";
	graph.valueField = "mobile_to_phone";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#00CC00";
	chart.addGraph(graph);

	// 10th graph
	var graph = new AmCharts.AmGraph();
	graph.title = "mobile_to_pad";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[title]])";
	graph.valueField = "mobile_pad";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#99FF99";
	chart.addGraph(graph);

	// 11th graph
	var graph = new AmCharts.AmGraph();
	graph.title = "mobile_to_pc";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[title]])";
	graph.valueField = "plug_in_to_pc";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#99FFFF";
	chart.addGraph(graph);
    
	// 12th graph
	var graph = new AmCharts.AmGraph();
	graph.title = "mobile_to_unknown";
	graph.labelText = "[[value]]";
	graph.balloonText = "[[value]] ([[title]])";
	graph.valueField = "mobile_to_unknown";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#CCFF33";
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
	tmp.setDate(26);
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
                                share_to_phone : data[i].share.phone,
                                share_to_pad : data[i].share.pad,
                                share_to_pc : data[i].share.pc,
                                share_to_unknown : data[i].share.unknown,
								plug_in_to_pad : data[i].plug_in.phone,
								plug_in_to_pad : data[i].plug_in.pad,
								plug_in_to_pc : data[i].plug_in.pc,
								plug_in_to_unknown : data[i].plug_in.unknown,
								mobile_to_phone : data[i].mobile.phone,
								mobile_to_pad : data[i].mobile.pad,
								mobile_to_pc : data[i].mobile.pc,
								mobile_to_unknown : data[i].mobile.unknown
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

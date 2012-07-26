var make_activate_user_chart = function(chartData, radio_type) {
	var e = document.getElementById('depth_activate_user')
	clearElement(e);

	// SERIAL CHART
	chart = new AmCharts.AmSerialChart();
	chart.dataProvider = chartData;
	chart.categoryField = "time";
	chart.addTitle('活跃用户', 20);

	// AXES
	// category
	var categoryAxis = chart.categoryAxis;
	categoryAxis.gridAlpha = 0.1;
	categoryAxis.axisAlpha = 0;
	categoryAxis.gridPosition = "start";

	// value
	var valueAxis = new AmCharts.ValueAxis();
	valueAxis.stackType = "regular";
	valueAxis.gridAlpha = 0.1;
	valueAxis.axisAlpha = 0;
	chart.addValueAxis(valueAxis);

	var valueAxis2 = new AmCharts.ValueAxis();
	valueAxis2.position = "right";
	valueAxis2.axisColor = "#FCD202";
	valueAxis2.gridAlpha = 0;
	valueAxis2.axisThickness = 1;
	chart.addValueAxis(valueAxis2);

	// first graph
	graph = new AmCharts.AmGraph();
	graph.title = "活跃用户";
	graph.labelText = "[[value]]";
	graph.valueField = "au";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#DB4C3C";
	chart.addGraph(graph);

	// second graph
	var graph = new AmCharts.AmGraph();
	graph.title = "注册用户";
	graph.labelText = "[[value]]";
	graph.valueField = "reg";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	graph.lineColor = "#DAF0FD";
	chart.addGraph(graph);

	// third graph
	var graph2 = new AmCharts.AmGraph();
	graph2.title = "yellow line";
	graph2.valueField = "percent";
	graph2.bullet = "round";
	graph2.valueAxis = valueAxis2;
	graph2.hideBulletsCount = 50;
	graph2.lineColor = "#FCD202";
	if (radio_type == 1) {
		chart.addGraph(graph2);
	}

	// LEGEND
	var legend = new AmCharts.AmLegend();
	legend.borderAlpha = 0.2;
	legend.horizontalGap = 10;
	chart.addLegend(legend);

	// WRITE
	chart.write(e.getAttribute('id'));
};

var load_activate_user = function(params, callback) {
	url = '/statistics/depth/activate_user';

	var from = $("#depth_activate_user_from").val()
	var to = $("#depth_activate_user_to").val()

	var date_range = get_date_range(from, to);
	var data_grain = $("#table_activate_user #data_grain").val();
	var radio_type = parseInt($("#table_activate_user :radio:checked").val(),
			10);

	var params = {
		start_time : date_range.start_time,
		end_time : date_range.end_time,
		data_grain : data_grain
	};

	var e = document.getElementById('depth_activate_user')
	clearElement(e);
	var loading = document.createElement('p')
	var loading_text = document.createTextNode('数据加载中...')
	loading.appendChild(loading_text);
	e.appendChild(loading);

	make_activate_user_chart(null, radio_type);
	myAjax(url, params, function(obj) {
				data = obj.list;
				len = data.length;
				chartData = [];
				for (var i = 0; i < len; i++) {
					chartData.push({
								time : data[i].time,
								reg : data[i].reg,
								au : data[i].au,
								percent : data[i].percent
							});
				}
				make_activate_user_chart(chartData, radio_type);
				prepare_activate_user.chartData = chartData;
				if (callback && typeof callback == 'function') {
					callback();
				}
			});
};

var prepare_activate_user = function() {
	$("#depth_activate_user_from").datepicker({
		changeMonth : true,
		numberOfMonths : 2,
		dateFormat : "yy-mm-dd",
		onSelect : function(selectedDate) {
			$("#depth_activate_user_to").datepicker("option", "minDate",
					selectedDate);
		}
	});
	$("#depth_activate_user_to").datepicker({
				changeMonth : true,
				numberOfMonths : 2,
				dateFormat : "yy-mm-dd"
			});
	$("#table_activate_user :radio").change(function() {
		var radio_type = parseInt($("#table_activate_user :radio:checked")
						.val(), 10);
		alert(radio_type)
		if (prepare_activate_user.chartData) {
			make_activate_user_chart(chartData, radio_type);
		} else {
			load_activate_user();
		}
	});
	$("#table_activate_user #data_grain").change(load_activate_user);
	$("#table_activate_user #submit").click(load_activate_user);
	$("#table_activate_user #reset").click(function() {
				$("#depth_activate_user_from").val('');
				$("#depth_activate_user_to").val('');
			});

	load_activate_user();
};


$(document).ready(function() {
			prepare_activate_user();
		});

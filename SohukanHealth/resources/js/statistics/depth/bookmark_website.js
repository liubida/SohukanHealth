var make_bookmark_website_chart = function(chartData) {
	var e = document.getElementById('depth_bookmark_website')
	clearElement(e);

	// SERIAL CHART
	chart = new AmCharts.AmSerialChart();
	chart.dataProvider = chartData;
	chart.categoryField = "domain";
	chart.startDuration = 1;
	chart.addTitle('文章来源网站(PV)', 20);

	// AXES
	// category
	var categoryAxis = chart.categoryAxis;
	categoryAxis.labelRotation = 90;
	categoryAxis.gridPosition = "start";

	// GRAPH
	var graph = new AmCharts.AmGraph();
	graph.valueField = "count";
	graph.balloonText = "[[category]]: [[value]]";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 0.8;
	chart.addGraph(graph);

	chart.write(e.getAttribute('id'));
};

var load_bookmark_website = function(params, callback) {
	url = '/statistics/depth/bookmark_website';

	var now = new Date();
	var to = $("#depth_bookmark_website_to").val();
	to = to || now.format('yyyy-MM-dd hh:mm:ss');
	
	var from = $("#depth_bookmark_website_from").val();
	tmp = now;
	tmp.setMonth(now.getMonth() - 1)
	from = from || tmp.format('yyyy-MM-dd hh:mm:ss');
	
	var date_range = get_date_range(from, to);
	var size = $("#table_bookmark_website #size").val();

	var params = {
		start_time : date_range.start_time,
		end_time : date_range.end_time,
		size : size
	};

	var e = document.getElementById('depth_bookmark_website')
	clearElement(e);
	var loading = document.createElement('p')
	var loading_text = document.createTextNode('数据加载中...')
	loading.appendChild(loading_text);
	e.appendChild(loading);

	myAjax(url, params, function(obj) {
				data = obj.list;
				len = data.length;
				make_bookmark_website_chart(data);
				prepare_bookmark_website.data = data;

				if (callback && typeof callback == 'function') {
					callback();
				}
				$("#depth_bookmark_website_from").val(from.substr(0,10));
				$("#depth_bookmark_website_to").val(to.substr(0,10));
			});
};

var prepare_bookmark_website = function() {
	$("#depth_bookmark_website_from").datepicker({
		changeMonth : true,
		numberOfMonths : 2,
		dateFormat : "yy-mm-dd",
		onSelect : function(selectedDate) {
			$("#depth_bookmark_website_to").datepicker("option", "minDate",
					selectedDate);
		}
	});
	$("#depth_bookmark_website_to").datepicker({
				changeMonth : true,
				numberOfMonths : 2,
				dateFormat : "yy-mm-dd"
			});
	$("#table_bookmark_website #submit").click(load_bookmark_website);
	$("#table_bookmark_website #reset").click(function() {
				$("#depth_bookmark_website_from").val('');
				$("#depth_bookmark_website_to").val('');
			});

	load_bookmark_website();
};

$(document).ready(function() {
			prepare_bookmark_website();
		});
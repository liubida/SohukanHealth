var make_bookmark_per_user_chart = function(chartData) {
	var e = document.getElementById('bookmark_per_user_div')
	clearElement(e);

	// SERIAL CHART
	var chart = new AmCharts.AmSerialChart();
	chart.dataProvider = chartData;
	chart.categoryField = "user_id";
	chart.startDuration = 1;
	chart.addTitle('文章数/用户ID(前100名)', 20);

	// AXES
	// category
	var categoryAxis = chart.categoryAxis;
	categoryAxis.labelRotation = 45; // this line makes category
	// values to be rotated
	categoryAxis.gridAlpha = 0;
	categoryAxis.fillAlpha = 1;
	categoryAxis.fillColor = "#FAFAFA";
	categoryAxis.gridPosition = "start";

	// value
	var valueAxis = new AmCharts.ValueAxis();
	valueAxis.dashLength = 5;
	valueAxis.title = "bookmark num"
	valueAxis.axisAlpha = 0;
	chart.addValueAxis(valueAxis);

	// GRAPH
	var graph = new AmCharts.AmGraph();
	graph.valueField = "count";
	graph.colorField = "color";
	graph.balloonText = "[[category]]: [[value]]";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 1;
	chart.addGraph(graph);

	// WRITE
	chart.write("bookmark_per_user_div");
};

var load_bookmark_per_user = function(params, callback) {
	url = '/statistics/bookmark/per_user';

	var e = document.getElementById('bookmark_per_user_div')
	clearElement(e);

	var loading = document.createElement('p')
	var loading_text = document.createTextNode('数据加载中...')
	loading.appendChild(loading_text);
	e.appendChild(loading);

	myAjax(url, params, function(obj) {
				data = obj.list;
				len = data.length;
				chartData = [];
				for (var i = 0; i < len; i++) {
					chartData.push({
								user_id : data[i].user_id,
								count : data[i].count,
								color : data[i].color
							});
				}
				make_bookmark_per_user_chart(chartData);
				if (callback && typeof callback == 'function') {
					callback();
				}
			});
};

var create_ul_for_per_user = function() {
	var today = new Date();
	var tmp = new Date();
	var time_array = [{
		'text' : '昨天',
		'value' : tmp.setDate(today.getDate() - 1) ? tmp
				.format('yyyy.MM.dd hh:mm:ss') : null
	}, {
		'text' : '7天',
		'value' : tmp.setDate(today.getDate() - 7) ? tmp
				.format('yyyy.MM.dd hh:mm:ss') : null
	}, {
		'text' : '30天',
		'value' : tmp.setMonth(today.getMonth() - 1) ? tmp
				.format('yyyy.MM.dd hh:mm:ss') : null
	}, {
		'text' : '3个月',
		'value' : tmp.setMonth(today.getMonth() - 3) ? tmp
				.format('yyyy.MM.dd hh:mm:ss') : null
	}, {
		'text' : '6个月',
		'value' : tmp.setMonth(today.getMonth() - 6) ? tmp
				.format('yyyy.MM.dd hh:mm:ss') : null
	}, {
		'text' : '1年',
		'value' : tmp.setFullYear(today.getFullYear() - 1) ? tmp
				.format('yyyy.MM.dd hh:mm:ss') : null
	}];
	var ul = document.createElement('ul');
	for (var i = 0; i < time_array.length; i++) {
		var li = document.createElement('li');
		addClass(li, 'heng_li');

		var a = create_link(i, time_array[i]['text'], time_array[i]['value'],
				function() {
					var t = this.firstChild;
					var old_nodeValue = t.nodeValue;
					t.nodeValue = '请求数据中';

					load_bookmark_per_user({
								start_time : this.getAttribute('value')
							}, function() {
								t.nodeValue = old_nodeValue;
							});
					return false;
				});
		li.appendChild(a);
		ul.appendChild(li)
	}
	return ul;
};

var prepare_bookmark_per_user = function() {
	var div = document.getElementById('bookmark_per_user_div');

	var ul = create_ul_for_per_user();
	var link_div = document.createElement('div');
	link_div.style.float = 'left';
	link_div.appendChild(ul);
	insertAfter(link_div, div);
	load_bookmark_per_user();
};

AmCharts.ready(function() {
			prepare_bookmark_per_user();
		});

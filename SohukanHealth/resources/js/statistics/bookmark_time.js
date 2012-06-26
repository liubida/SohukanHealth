var make_bookmark_time_chart = function(chartData) {
	var e = document.getElementById('bookmark_time_div')
	clearElement(e);

	// SERIAL CHART
	var chart = new AmCharts.AmSerialChart();
	chart.dataProvider = chartData;
	chart.categoryField = "hour";
	chart.startDuration = 1;
	chart.addTitle('添加文章数/分时段', 20);

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
	chart.write("bookmark_time_div");
};

var load_bookmark_time = function(params, callback) {
	url = '/statistics/bookmark/time';

	var e = document.getElementById('bookmark_time_div')
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
								hour : data[i].hour,
								count : data[i].count,
								color : data[i].color
							});
				}
				make_bookmark_time_chart(chartData);
				if (callback && typeof callback == 'function') {
					callback();
				}
			});
};

var create_link = function(url, text, value) {
	var a = document.createElement('a');
	var a_text = document.createTextNode(text);

	a.setAttribute('href', url);
	a.setAttribute('value', value);
	addClass(a, 'normal_a');

	a.onclick = function() {
		var t = a.firstChild;
		var old_nodeValue = t.nodeValue;
		t.nodeValue = '请求数据中';

		load_bookmark_time({
					start_time : this.getAttribute('value')
				}, function() {
					t.nodeValue = old_nodeValue;
				});
		return false;
	};

	a.appendChild(a_text);

	return a;
};

var create_ul = function() {
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

		var a = create_link(i, time_array[i]['text'], time_array[i]['value']);
		li.appendChild(a);
		ul.appendChild(li)
	}
	return ul;
};

var prepare_bookmark_time = function() {
	var div = document.getElementById('bookmark_time_div');

	var link_div = document.createElement('div');
	link_div.style.float = 'left';

	var ul = create_ul();
	link_div.appendChild(ul)
	insertAfter(link_div, div);
	load_bookmark_time(null, null);
};

AmCharts.ready(function() {
			prepare_bookmark_time();
		});

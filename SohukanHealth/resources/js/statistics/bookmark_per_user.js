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

var create_link = function(url, text) {
	var a = document.createElement('a');
	var a_text = document.createTextNode(text);

	a.setAttribute('href', url);
	addClass(a, 'normal_a');

	a.appendChild(a_text);
	return a;
};

var prepare_bookmark_per_user = function() {
	var div = document.getElementById('bookmark_per_user_div');

	var a1 = create_link('', '所有用户');
	a1.onclick = function() {
		var t = a1.firstChild;
		t.nodeValue = '请求数据中...';

		load_bookmark_per_user({
					includeTest : true
				}, function() {
					t.nodeValue = '所有用户';
				});
		return false;
	};

	var a2 = create_link('', '真实用户');
	a2.onclick = function() {
		var t = a2.firstChild;
		t.nodeValue = '请求数据中...';

		load_bookmark_per_user({
					includeTest : false
				}, function() {
					t.nodeValue = '真实用户';
				});
		return false;
	};
	var link_div = document.createElement('div');
	link_div.style.float = 'left';
	link_div.appendChild(a1);
	link_div.appendChild(a2);

	insertAfter(link_div, div);
	load_bookmark_per_user(null, null);
};

AmCharts.ready(function() {
			prepare_bookmark_per_user();
		});

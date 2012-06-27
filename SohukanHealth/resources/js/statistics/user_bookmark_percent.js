var make_user_bookmark_percent_chart = function(chartData) {
	var e = document.getElementById('user_bookmark_percent_div')
	clearElement(e);

	var chart = new AmCharts.AmPieChart();
	chart.addTitle("用户收藏文章统计", 20);

	chart.dataProvider = chartData;
	chart.titleField = "name";
	chart.valueField = "count";
	chart.sequencedAnimation = true;
	chart.startEffect = "elastic";
	chart.innerRadius = "30%";
	chart.startDuration = 0.5;
	chart.labelRadius = 15;

	// the following two lines makes the chart 3D
	chart.depth3D = 10;
	chart.angle = 15;

	// WRITE
	chart.write("user_bookmark_percent_div");
};

var load_user_bookmark_percent = function(params, callback) {
	url = '/statistics/user/bookmark_percent'

	var e = document.getElementById('user_bookmark_percent_div')
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
								name : data[i].name,
								count : data[i].count
							});
				}
				make_user_bookmark_percent_chart(chartData);
			});
};

var prepare_user_bookmark_percent = function() {
	var div = document.getElementById('user_bookmark_percent_div');

	var a1 = create_link('', '真实用户');
	a1.onclick = function() {
		var t = a1.firstChild;
		var old_nodeValue = t.nodeValue;
		t.nodeValue = '请求数据中...';

		load_user_bookmark_percent({
					includeTest : false
				}, function() {
					t.nodeValue = old_nodeValue;
				});
		return false;
	};

	var a2 = create_link('', '所有用户');
	a2.onclick = function() {
		var t = a2.firstChild;
		var old_nodeValue = t.nodeValue;
		t.nodeValue = '请求数据中...';

		load_user_bookmark_percent({
					includeTest : true
				}, function() {
					t.nodeValue = old_nodeValue;
				});
		return false;
	};
	var link_div = document.createElement('div');
	link_div.style.float = 'left';
	link_div.appendChild(a1);
	link_div.appendChild(a2);

	insertAfter(link_div, div);
	load_user_bookmark_percent();
};

AmCharts.ready(function() {
			prepare_user_bookmark_percent();
		});
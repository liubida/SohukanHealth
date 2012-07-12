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

var create_ul_for_percent = function() {
	var today = new Date();
	var tmp = new Date();
	var time_array = [{
		'text' : '昨天',
		'value' : tmp.setDate(today.getDate() - 1) ? tmp
				.format('yyyy.MM.dd hh:mm:ss') : null
	}, {
		'text' : '7天前',
		'value' : tmp.setDate(today.getDate() - 7) ? tmp
				.format('yyyy.MM.dd hh:mm:ss') : null
	}, {
		'text' : '30天前',
		'value' : tmp.setMonth(today.getMonth() - 1) ? tmp
				.format('yyyy.MM.dd hh:mm:ss') : null
	}, {
		'text' : '3个月前',
		'value' : tmp.setMonth(today.getMonth() - 3) ? tmp
				.format('yyyy.MM.dd hh:mm:ss') : null
	}, {
		'text' : '6个月前',
		'value' : tmp.setMonth(today.getMonth() - 6) ? tmp
				.format('yyyy.MM.dd hh:mm:ss') : null
	}, {
		'text' : '1年前',
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

					load_user_bookmark_percent({
								before_time : this.getAttribute('value')
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
var prepare_user_bookmark_percent = function() {
	var div = document.getElementById('user_bookmark_percent_div');

	// var ul = create_ul_for_percent();
	// var link_div = document.createElement('div');
	// link_div.style.float = 'left';
	// link_div.appendChild(ul);
	// insertAfter(link_div, div);
	load_user_bookmark_percent();
};

AmCharts.ready(function() {
			prepare_user_bookmark_percent();
		});
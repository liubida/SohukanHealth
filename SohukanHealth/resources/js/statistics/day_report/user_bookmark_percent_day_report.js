var make_user_bookmark_percent_chart = function(chartData) {
	var div = document.getElementById('user_bookmark_percent_day_report_div');
	clearElement(div);

	var chart = new AmCharts.AmPieChart();
//	chart.addTitle("用户收藏文章统计", 20);

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
	chart.write(div.getAttribute('id'));
};

var load_user_bookmark_percent = function(params, callback) {
	url = '/statistics/day_report/bookmark_percent'

	var div = document.getElementById('user_bookmark_percent_day_report_div');
	clearElement(div);

	var loading = document.createElement('p')
	var loading_text = document.createTextNode('数据加载中...')
	loading.appendChild(loading_text);
	div.appendChild(loading);

	var raw_div = document
			.getElementById('user_bookmark_percent_day_report_raw_div');
	clearElement(raw_div);
	
	myAjax(url, params, function(obj) {
				if (callback && typeof callback == 'function') {
					callback();
				}
				// 源数据填充表格
				data = obj.data;
				// percent数据绘制饼图
				percent = obj.percent;

				// 绘图
				chartData = [];
				for (var i = 0; i < percent.length; i++) {
					chartData.push({
								name : percent[i].name,
								count : percent[i].count
							});
				}
				make_user_bookmark_percent_chart(chartData);

				var table = document.createElement('table')
				var tr1 = document.createElement('tr')
				var tr2 = document.createElement('tr')

				var td = document.createElement('td');
				var td_text = document.createTextNode("文章数");
				td.appendChild(td_text);
				tr1.appendChild(td);

				var td = document.createElement('td');
				var td_text = document.createTextNode("用户数");
				td.appendChild(td_text);
				tr2.appendChild(td);

				for (var i = 0; i < data.length; i++) {
					var td = document.createElement('td');
					var td_text = document.createTextNode(data[i].p_count);
					td.appendChild(td_text);
					tr1.appendChild(td);

					var td = document.createElement('td');
					var td_text = document.createTextNode(data[i].u_count);
					td.appendChild(td_text);

					tr2.appendChild(td);
				}
				table.appendChild(tr1);
				table.appendChild(tr2);
				raw_div.appendChild(table);
			});
};

var prepare_user_bookmark_percent = function() {
	// var div =
	// document.getElementById('user_bookmark_percent_day_report_div');
	// var ul = create_ul_for_percent();
	// var link_div = document.createElement('div');
	// link_div.style.float = 'left';
	// link_div.appendChild(ul);
	// insertAfter(link_div, div);
	// var today = new Date();
	var day_str = '2012-07-16';
	var da = day_str.split("-");
	var da_int = [];
	for (var i = 0; i < da.length; i++) {
		da_int[i] = parseInt(da[i],10);
	}
	var day = new Date(da_int[0], da_int[1] - 1, da_int[2], 0, 0, 0);
	var tmp = new Date(da_int[0], da_int[1] - 1, da_int[2] + 1, 0, 0, 0);

//	alert(day.format('yyyy.MM.dd hh:mm:ss'));
//	alert(tmp.format('yyyy.MM.dd hh:mm:ss'));
	
	load_user_bookmark_percent({
				start_time : day.format('yyyy-MM-dd hh:mm:ss'),
				end_time : tmp.format('yyyy-MM-dd hh:mm:ss')
			});
};

//AmCharts.ready(function() {
//			prepare_user_bookmark_percent();
//		});
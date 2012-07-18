var make_user_bookmark_website_chart = function(chartData) {
	var div = document.getElementById('user_bookmark_website_day_report_div');
	clearElement(div);
	//
	// var chart = new AmCharts.AmPieChart();
	// chart.addTitle("收藏文章来源网站", 20);
	//
	// chart.dataProvider = chartData;
	// chart.titleField = "name";
	// chart.valueField = "count";
	// chart.sequencedAnimation = true;
	// chart.startEffect = "elastic";
	// chart.innerRadius = "30%";
	// chart.startDuration = 0.5;
	// chart.labelRadius = 15;
	//
	// // the following two lines makes the chart 3D
	// chart.depth3D = 10;
	// chart.angle = 15;
	//
	// // WRITE
	// chart.write(div.getAttribute('id'));
	//	

	// SERIAL CHART
	chart = new AmCharts.AmSerialChart();
	chart.dataProvider = chartData;
	chart.categoryField = "domain";
	chart.startDuration = 1;

	// AXES
	// category
	var categoryAxis = chart.categoryAxis;
	categoryAxis.labelRotation = 90;
	categoryAxis.gridPosition = "start";

	// value
	// in case you don't want to change default settings of value axis,
	// you don't need to create it, as one value axis is created automatically.

	// GRAPH
	var graph = new AmCharts.AmGraph();
	graph.valueField = "count";
	graph.balloonText = "[[category]]: [[value]]";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 0.8;
	chart.addGraph(graph);

	chart.write(div.getAttribute('id'));

};

var load_user_bookmark_website = function(params, callback) {
	url = '/statistics/day_report/bookmark_website'

	var div = document.getElementById('user_bookmark_website_day_report_div');
	clearElement(div);

	var loading = document.createElement('p')
	var loading_text = document.createTextNode('数据加载中...')
	loading.appendChild(loading_text);
	div.appendChild(loading);

	var raw_div = document
			.getElementById('user_bookmark_website_day_report_raw_div');
	clearElement(raw_div);
	
	myAjax(url, params, function(obj) {
				if (callback && typeof callback == 'function') {
					callback();
				}
				data = obj.data;
				len = data.length;

				// 绘图
				chartData = [];
				for (var i = 0; i < len; i++) {
					chartData.push({
								domain : data[i].domain,
								count : data[i].count
							});
				}
				make_user_bookmark_website_chart(chartData);

				var table = document.createElement('table')
				var th1 = document.createElement('th')
				var th1_text = document.createTextNode("网站");
				th1.appendChild(th1_text);
				var th2 = document.createElement('th')
				var th2_text = document.createTextNode("文章数");
				th2.appendChild(th2_text);

				table.appendChild(th1);
				table.appendChild(th2);

				for (var i = 0; i < data.length; i++) {
					var tr = document.createElement('tr')
					var td = document.createElement('td');
					var td_text = document.createTextNode(data[i].domain);
					td.appendChild(td_text);
					tr.appendChild(td);

					var td = document.createElement('td');
					var td_text = document.createTextNode(data[i].count);
					td.appendChild(td_text);
					tr.appendChild(td);

					table.appendChild(tr);
				}
				raw_div.appendChild(table);
			});
};

var prepare_user_bookmark_website = function() {
	var div = document.getElementById('user_bookmark_website_day_report_div');
	// var ul = create_ul_for_percent();
	// var link_div = document.createElement('div');
	// link_div.style.float = 'left';
	// link_div.appendChild(ul);
	// insertAfter(link_div, div);
	var day_str = '2012-07-16';
	var da = day_str.split("-");
	var da_int = [];
	for (var i = 0; i < da.length; i++) {
		da_int[i] = parseInt(da[i]);
	}
	var day = new Date(da_int[0], da_int[1] - 1, da_int[2], 0, 0, 0);
	var tmp = new Date(da_int[0], da_int[1] - 1, da_int[2] + 1, 0, 0, 0);

	load_user_bookmark_website({
				start_time : day.format('yyyy-MM-dd hh:mm:ss'),
				end_time : tmp.format('yyyy-MM-dd hh:mm:ss')
			});
};

// AmCharts.ready(function() {
// prepare_user_bookmark_website();
// });

var make_user_bookmark_percent_chart = function(chartData) {
	var e = document.getElementById('statistics_bookmark_percent_div')
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
	chart.write(e.getAttribute('id'));
};

var load_bookmark_percent = function(params, callback) {
	url = '/statistics/user/bookmark_percent'

	var from = $("#statistics_bookmark_percent_from").val()
	var to = $("#statistics_bookmark_percent_to").val()
	var date_range = get_date_range(from, to);

	// TODO params
	var params = {
		start_time : date_range.start_time,
		end_time : date_range.end_time
	};

	var e = document.getElementById('statistics_bookmark_percent_div')
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
								name : data[i].name,
								count : data[i].count
							});
				}
				make_user_bookmark_percent_chart(chartData);
				prepare_bookmark_percent.chartData = chartData;

				if (callback && typeof callback == 'function') {
					callback();
				}
			});
};

var prepare_bookmark_percent = function() {
	$("#statistics_bookmark_percent_from").datepicker({
		changeMonth : true,
		numberOfMonths : 2,
		dateFormat : "yy-mm-dd"
			// ,
			// onSelect : function(selectedDate) {
			// $("#statistics_bookmark_percent_to").datepicker("option",
			// "minDate", selectedDate);
			// }
		});
	$("#statistics_bookmark_percent_to").datepicker({
				changeMonth : true,
				numberOfMonths : 2,
				dateFormat : "yy-mm-dd"
			});
	$("#table_bookmark_percent #submit").click(load_bookmark_percent);
	$("#table_bookmark_percent #reset").click(function() {
				$("#statistics_bookmark_percent_from").val('');
				$("#statistics_bookmark_percent_to").val('');
			});
	load_bookmark_percent();
};

$(document).ready(function() {
			prepare_bookmark_percent();
		});
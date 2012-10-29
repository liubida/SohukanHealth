var load_week_report_abstract = function(params, callback) {
	var url = '/statistics/week_report/abstract';
	var e = document.getElementById('week_report_abstract');

	if (e) {
		clearElement(e);

		var loading = document.createElement('p')
		var loading_text = document.createTextNode('数据加载中...')
		loading.appendChild(loading_text);
		e.appendChild(loading);
	}
	url = url + '?start_time=' + params
	$('#week_report_abstract').load(url);

	var div_content = document.getElementById('week_report_content');
	div_content.style.display = 'block';
};

var load_week_report_add_way_and_platform = function(params, callback) {
	var url = "statistics/week_report/add_way_and_platform";
	var e = document.getElementById('week_report_add_way_and_platform');

	if (e) {
		clearElement(e);
		var loading = document.createElement('p')
		var loading_text = document.createTextNode('数据加载中...')
		loading.appendChild(loading_text);
		e.appendChild(loading);
	}
	url = url + '?start_time' + params
	$('week_report_add_way_and_platform').load(url);
};

var prepare_week_report = function() {
	var url = '/statistics/week_report/date/'

	var div_content = document.getElementById('week_report_content');
	div_content.style.display = 'none';

	var div_date = document.getElementById('week_report_date');
	div_date.appendChild(document.createElement('p'));

	$('#week_report_date').load(url, function() {
		$('#week_report_date a').click(function() {
			load_week_report_abstract(this.id);
			load_week_report_add_way_and_platform(this.id);
			$('#week_report_date a').attr('class', 'pageNum');
			$(this).attr('class', 'currentPage');

			
			div_content.style.display = 'block';
			var day_str = this.id;
			var da = day_str.split("-");
			var da_int = [];
			for (var i = 0; i < da.length; i++) {
				da_int[i] = parseInt(da[i], 10);
			}

			var day = new Date(da_int[0], da_int[1] - 1, da_int[2], 0, 0, 0);
			var tmp = new Date(da_int[0], da_int[1] - 1, da_int[2] + 6, 0, 0, 0);
			var start_time = day.format('yyyy-MM-dd hh:mm:ss');
			var end_time = tmp.format('yyyy-MM-dd hh:mm:ss');

			load_user_bookmark_website({
						start_time : start_time,
						end_time : end_time
					});
			return false;
		});

		var now = new Date();
		// 获取7天前的日期
		now.setDate(now.getDate() - 7);
		$('#week_report_date a').each(function() {
					var day_str = this.id;
					var da = day_str.split("-");
					var da_int = [];
					for (var i = 0; i < da.length; i++) {
						da_int[i] = parseInt(da[i], 10);
					}

					var day = new Date(da_int[0], da_int[1] - 1, da_int[2], 0,
							0, 0);
					var diff = parseInt((now - day) / 86400000, 10)
					if (diff < 7) {
						$('#' + this.id).click();
					}
				});
	});
};

$(document).ready(function() {
			prepare_week_report();
		});

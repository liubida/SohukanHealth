var load_week_report_abstract = function(params, callback) {
	var url = '/statistics/week_report/abstract/';
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

var prepare_week_report = function() {
	var url = '/statistics/week_report/date/'

	var div_content = document.getElementById('week_report_content');
	div_content.style.display = 'none';

	var div_date = document.getElementById('week_report_date');
	div_date.appendChild(document.createElement('p'));

	$('#week_report_date').load(url, function() {
		$('#week_report_date a').click(function() {
			load_week_report_abstract(this.id);
			$('#week_report_date a').attr('class', 'pageNum');
			$(this).attr('class', 'currentPage');

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

	//	
	// myAjax(url, {}, function(obj) {
	// data = obj.list;
	// for (var i = 0; i < data.length; i++) {
	// var a = document.createElement('a');
	// a.setAttribute('id', data[i]);
	// a.setAttribute('href', data[i]);
	// a.setAttribute('title', data[i]);
	// a.className = 'pageNum';
	//
	// var day_str = '2012-' + data[i];
	// (function (day_str) {
	// a.onclick = function() {
	// var date_div = document
	// .getElementById('week_report_date');
	// var links = date_div.getElementsByTagName('a');
	// for (var i = 0; i < links.length; i++) {
	// links[i].className = 'pageNum';
	// }
	// this.className = 'currentPage';
	//
	// div_content.style.display = 'block';
	//
	// var da = day_str.split("-");
	// var da_int = [];
	// for (var i = 0; i < da.length; i++) {
	// da_int[i] = parseInt(da[i], 10);
	// }
	// var day = new Date(da_int[0], da_int[1] - 1,
	// da_int[2], 0, 0, 0);
	// var tmp = new Date(da_int[0], da_int[1] - 1,
	// da_int[2] + 1, 0, 0, 0);
	// var start_time = day.format('yyyy-MM-dd hh:mm:ss');
	// var end_time = tmp.format('yyyy-MM-dd hh:mm:ss');
	// load_week_report_abstract({
	// start_time : start_time,
	// end_time : end_time
	// });
	// load_user_bookmark_percent({
	// start_time : start_time,
	// end_time : end_time
	// });
	// load_user_bookmark_website({
	// start_time : start_time,
	// end_time : end_time
	// });
	// return false;
	// };
	// })(day_str)
	//
	// var a_text = document.createTextNode(data[i]);
	// a.appendChild(a_text);
	// div_date.appendChild(a);
	// }
	//
	// });
};

var load_week_report_abstract1 = function(params) {
	var url = '/statistics/week_report/abstract'
	var week_report_user = document.getElementById('week_report_user');
	var week_report_bookmark = document.getElementById('week_report_bookmark');

	var user_total = document.getElementById('week_report_user_total');
	clearElement(user_total);
	var user_new = document.getElementById('week_report_user_new');
	clearElement(user_new);
	var bookmark_total = document.getElementById('week_report_bookmark_total');
	clearElement(bookmark_total);
	var bookmark_new = document.getElementById('week_report_bookmark_new');
	clearElement(bookmark_new);

	myAjax(url, params, function(obj) {
		data = obj;
		var value = document.createTextNode(data['user_total'] + ' ');
		var inc = document.createElement('font');
		inc.style.color = '#c00';
		var inc_text = document.createTextNode('['
				+ (parseFloat(data['user_total_inc']) * 100).toFixed(2) + '%]');
		inc.appendChild(inc_text);
		user_total.appendChild(value);
		user_total.appendChild(inc);

		var value = document.createTextNode(data['user_new'] + ' ');
		var inc = document.createElement('font');
		inc.style.color = data['user_new_inc_color'];
		var inc_text = document.createTextNode('['
				+ (parseFloat(data['user_new_inc']) * 100).toFixed(2) + '%]');
		inc.appendChild(inc_text);
		user_new.appendChild(value);
		user_new.appendChild(inc);

		var value = document.createTextNode(data['bookmark_total'] + ' ');
		var inc = document.createElement('font');
		inc.style.color = '#c00';
		var inc_text = document.createTextNode('['
				+ (parseFloat(data['bookmark_total_inc']) * 100).toFixed(2)
				+ '%]');
		inc.appendChild(inc_text);
		bookmark_total.appendChild(value);
		bookmark_total.appendChild(inc);

		var value = document.createTextNode(data['bookmark_new'] + ' ');
		var inc = document.createElement('font');
		inc.style.color = data['bookmark_new_inc_color'];
		var inc_text = document.createTextNode('['
				+ (parseFloat(data['bookmark_new_inc']) * 100).toFixed(2)
				+ '%]');
		inc.appendChild(inc_text);
		bookmark_new.appendChild(value);
		bookmark_new.appendChild(inc);
	});
}

$(document).ready(function() {
			prepare_week_report();
		});

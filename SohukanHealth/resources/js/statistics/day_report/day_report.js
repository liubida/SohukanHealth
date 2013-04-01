var prepare_day_report = function() {
	var url = '/statistics/day_report/date'

	var div_content = document.getElementById('day_report_content');
	div_content.style.display = 'none';

	var div_date = document.getElementById('day_report_date');
	div_date.appendChild(document.createElement('p'));

	myAjax(url, {}, function(obj) {
				data = obj.list;
				for (var i = 0; i < data.length; i++) {
					var a = document.createElement('a');
					a.setAttribute('id', data[i]);
					a.setAttribute('href', data[i]);
					a.setAttribute('title', data[i]);
					a.className = 'pageNum';
                    var day_str = data[i];
	(function		(day_str) {
						a.onclick = function() {
							var date_div = document
									.getElementById('day_report_date');
							var links = date_div.getElementsByTagName('a');
							for (var i = 0; i < links.length; i++) {
								links[i].className = 'pageNum';
							}
							this.className = 'currentPage';

							div_content.style.display = 'block';

							var da = day_str.split("-");
							var da_int = [];
							for (var i = 0; i < da.length; i++) {
								da_int[i] = parseInt(da[i], 10);
							}
							var day = new Date(da_int[0], da_int[1] - 1,
									da_int[2], 0, 0, 0);
							var tmp = new Date(da_int[0], da_int[1] - 1,
									da_int[2] + 1, 0, 0, 0);
							var start_time = day.format('yyyy-MM-dd hh:mm:ss');
							var end_time = tmp.format('yyyy-MM-dd hh:mm:ss');
							load_day_report_abstract({
										start_time : start_time,
										end_time : end_time
									});
							load_user_bookmark_percent({
										start_time : start_time,
										end_time : end_time
									});
							load_user_bookmark_website({
										start_time : start_time,
										end_time : end_time
									});
							return false;
						};
					})(day_str)

				    var tmp_str = data[i].split("-");
                    var display_str = tmp_str[1] + '-' + tmp_str[2];
					var a_text = document.createTextNode(display_str);
					a.appendChild(a_text);
					div_date.appendChild(a);
				}

				// ajax获取date之后, 自动触发一次昨天的click, 显示昨天的日报信息
				var now = new Date();
				// 获取昨天的日期
				now.setDate(now.getDate() - 1);
				$('#day_report_date a').each(function() {
                            var id_array = this.id.split("-")
							var year = id_array[0]
							var month = id_array[1]
							var day = id_array[2]
                            //alert(year+month+day)
                            //alert(now.getFullYear())
							if (now.getFullYear() == year && 
                                now.getMonth() + 1 == month &&
								now.getDate() == day) {
								$('#' + this.id).click();
							}
						});
			});
};

var load_day_report_abstract = function(params) {
	var url = '/statistics/day_report/abstract/'
	var day_report_user = document.getElementById('day_report_user');
	var day_report_bookmark = document.getElementById('day_report_bookmark');
	var day_report_email = document.getElementById('day_report_email');
	var day_report_fiction = document.getElementById('day_report_fiction');
	var day_report_shorturl = document.getElementById('day_report_shorturl');
	var day_report_set_public = document.getElementById('day_report_set_public');

	var user_total = document.getElementById('day_report_user_total');
	clearElement(user_total);
	var user_new = document.getElementById('day_report_user_new');
	clearElement(user_new);
	var bookmark_total = document.getElementById('day_report_bookmark_total');
	clearElement(bookmark_total);
	var bookmark_new = document.getElementById('day_report_bookmark_new');
	clearElement(bookmark_new);
	var bookmark_failed = document.getElementById('day_report_bookmark_failed');
	clearElement(bookmark_failed);
	var email_total = document.getElementById('day_report_email_total');
	clearElement(email_total);
	var email_new = document.getElementById('day_report_email_new');
	clearElement(email_new);
	var fiction_total = document.getElementById('day_report_fiction_total');
	clearElement(fiction_total);
	var fiction_new = document.getElementById('day_report_fiction_new');
	clearElement(fiction_new);
	var shorturl_total = document.getElementById('day_report_shorturl_total');
	clearElement(shorturl_total);
	var shorturl_new = document.getElementById('day_report_shorturl_new');
	clearElement(shorturl_new);
	var set_public_total = document.getElementById('day_report_set_public_total');
	clearElement(set_public_total);
	var set_public_new = document.getElementById('day_report_set_public_new');
	clearElement(set_public_new);

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

		var value = document.createTextNode(data['bookmark_failed_count']
				+ ' ['
				+ (parseFloat(data['bookmark_failed_percent']) * 100)
						.toFixed(2) + '%]');
		bookmark_failed.appendChild(value);

		var value = document.createTextNode(data['email_total'] + ' ');
		var inc = document.createElement('font');
		inc.style.color = '#c00';
		var inc_text = document.createTextNode('['
				+ (parseFloat(data['email_total_inc']) * 100).toFixed(2) + '%]');
		inc.appendChild(inc_text);
		email_total.appendChild(value);
		email_total.appendChild(inc);

		var value = document.createTextNode(data['email_new'] + ' ');
		var inc = document.createElement('font');
		inc.style.color = data['email_new_inc_color'];
		var inc_text = document.createTextNode('['
				+ (parseFloat(data['email_new_inc']) * 100).toFixed(2) + '%]');
		inc.appendChild(inc_text);
		email_new.appendChild(value);
		email_new.appendChild(inc);

		var value = document.createTextNode(data['fiction_total'] + ' ');
		var inc = document.createElement('font');
		inc.style.color = '#c00';
		var inc_text = document.createTextNode('['
				+ (parseFloat(data['fiction_total_inc']) * 100).toFixed(2)
				+ '%]');
		inc.appendChild(inc_text);
		fiction_total.appendChild(value);
		fiction_total.appendChild(inc);

		var value = document.createTextNode(data['fiction_new'] + ' ');
		var inc = document.createElement('font');
		inc.style.color = data['fiction_new_inc_color'];
		var inc_text = document.createTextNode('['
				+ (parseFloat(data['fiction_new_inc']) * 100).toFixed(2)
				+ '%]');
		inc.appendChild(inc_text);
		fiction_new.appendChild(value);
		fiction_new.appendChild(inc);

		var value = document.createTextNode(data['shorturl_total'] + ' ');
		var inc = document.createElement('font');
		inc.style.color = '#c00';
		var inc_text = document.createTextNode('['
				+ (parseFloat(data['shorturl_total_inc']) * 100).toFixed(2)
				+ '%]');
		inc.appendChild(inc_text);
		shorturl_total.appendChild(value);
		shorturl_total.appendChild(inc);

		var value = document.createTextNode(data['shorturl_new'] + ' ');
		var inc = document.createElement('font');
		inc.style.color = data['shorturl_new_inc_color'];
		var inc_text = document.createTextNode('['
				+ (parseFloat(data['shorturl_new_inc']) * 100).toFixed(2)
				+ '%]');
		inc.appendChild(inc_text);
		shorturl_new.appendChild(value);
		shorturl_new.appendChild(inc);

		var value = document.createTextNode(data['set_public_total'] + ' ');
		var inc = document.createElement('font');
		inc.style.color = '#c00';
		var inc_text = document.createTextNode('['
				+ (parseFloat(data['set_public_total_inc']) * 100).toFixed(2)
				+ '%]');
		inc.appendChild(inc_text);
		set_public_total.appendChild(value);
		set_public_total.appendChild(inc);

		var value = document.createTextNode(data['set_public_new'] + ' ');
		var inc = document.createElement('font');
		inc.style.color = data['set_public_new_inc_color'];
		var inc_text = document.createTextNode('['
				+ (parseFloat(data['set_public_new_inc']) * 100).toFixed(2)
				+ '%]');
		inc.appendChild(inc_text);
		set_public_new.appendChild(value);
		set_public_new.appendChild(inc);

	(function(bookmark_failed_array) {
			var array = bookmark_failed_array;
			bookmark_failed.onclick = function() {
				$('#box').empty().append('<div class="clearfix"></div>');
				var str_table = "<table id = 'table_bookmark_failed'><th>user_id</th><th>url</th></table>";
				$('#box div').append(str_table);
				$.blockUI({
							message : $('#box'),
							css : {
								top : '20%',
								left : '30%',
								textAlign : 'left',
								marginLeft : '-320px',
								marginTop : '-145px',
								background : 'none'
							}
						});
				$('.blockOverlay').attr('title', '单击关闭').click($.unblockUI);

				for (var i = 0; i < array.length; i++) {
					var tr = "<tr><td>" + array[i].user_id
							+ "</td><td><a href='" + array[i].url
							+ "' target='_blank'>" + array[i].url
							+ "</a></td></tr>";
					$('#table_bookmark_failed').append(tr);
				}
				$('#table_bookmark_failed').css({
							"width" : "800px",
							"font-size" : "12px"
						});
				$('#table_bookmark_failed td').css({
							"text-align" : "left"
						});
			}
		})(data['bookmark_failed']);
		$('#day_report_bookmark_failed').mouseover(function() {
			$('#day_report_bookmark_failed').css('background-color', '#DFF7F8');
		});
		$('#day_report_bookmark_failed').mouseout(function() {
					$('#day_report_bookmark_failed').css('background-color',
							'white');
				});
	});
}

var load_sys_alarm = function(params, callback) {
	// 加载系统可用率数据
	var url = '/monitor/sys_alarm/'
	var e = document.getElementById('sys_alarm')

	if (e) {
		clearElement(e);

		var loading = document.createElement('p')
		var loading_text = document.createTextNode('数据加载中...')
		loading.appendChild(loading_text);
		e.appendChild(loading);
	}
	url = url + params + '/'
	$('#sys_alarm').load(url);
};

$(document).ready(function() {
			prepare_day_report();
		});

Date.prototype.format = function(format) {
	var o = {
		"M+" : this.getMonth() + 1, // month
		"d+" : this.getDate(), // day
		"h+" : this.getHours(), // hour
		"m+" : this.getMinutes(), // minute
		"s+" : this.getSeconds(), // second
		"q+" : Math.floor((this.getMonth() + 3) / 3), // quarter
		"S" : this.getMilliseconds()
		// millisecond
	}

	if (/(y+)/.test(format)) {
		format = format.replace(RegExp.$1, (this.getFullYear() + "").substr(4
						- RegExp.$1.length));
	}
	for (var k in o) {
		if (new RegExp("(" + k + ")").test(format)) {
			format = format.replace(RegExp.$1, RegExp.$1.length == 1
							? o[k]
							: ("00" + o[k]).substr(("" + o[k]).length));
		}
	}
	return format;
}

var myAjax = function(url, params, callback) {
	$.ajax({
				url : url,
				type : 'get',
				data : params,
				timeout : 10000,
				async : true,
				beforeSend : function(XMLHttpRequest) {
				},
				complete : function(XMLHttpRequest, textStatus) {
				},
				success : function(data, textStatus) {
					jsonData = jQuery.parseJSON(data)
					// if (jsonData.success == true) {
					callback(jsonData);
					// } else {
					// alert('failed', "info:" + jsonData.info + " ,code:"
					// + jsonData.code);
					// }
				},
				error : function(XMLHttpRequest, textStatus, errorThrown) {
					// alert('没有响应', '服务器没有响应');
				}
			});
};

function insertAfter(newElement, targetElement) {
	var parent = targetElement.parentNode;
	if (parent.lastChild == targetElement) {
		parent.appendChild(newElement);
	} else {
		parent.insertBefore(newElement, targetElement.nextSibling);
	}
};

function addClass(element, value) {
	if (!element.className) {
		element.className = value;
	} else {
		newClassName = element.className;
		newClassName = newClassName + ' ' + value;
		element.className = newClassName;
	}
};

function clearElement(element) {
	if (!element)
		return;
	var child_nodes = element.childNodes;

	if (child_nodes) {
		for (var i = child_nodes.length - 1; i >= 0; i--) {
			element.removeChild(child_nodes[i]);
		}
	}
};

function addLoadEvent(func) {
	var old_onload = window.onload;
	if (typeof old_onload != 'function') {
		window.onload = func;
	} else {
		window.onload = function() {
			old_onload();
			func();
		}
	}
};

// ------------------

var create_link = function(url, text, value, onclick) {
	var a = document.createElement('a');
	var a_text = document.createTextNode(text);

	a.setAttribute('href', url);
	a.setAttribute('value', value);
	addClass(a, 'normal_a');

	if (onclick && typeof onclick == 'function') {
		a.onclick = onclick
	}

	a.appendChild(a_text);
	return a;
};

var chart_date_handler = function(time_str) {
	time = new Date(time_str);
	return time.format('MM.dd hh:mm');
};

var get_date_range = function(from, to) {
	var from_array = from ? from.split('-') : [];
	var from_int_array = [];
	for (var i = 0; i < from_array.length; i++) {
		from_int_array[i] = parseInt(from_array[i], 10);
	}
	var from_time = new Date(from_int_array[0], from_int_array[1] - 1,
			from_int_array[2], 0, 0, 0);

	var to_array = to ? to.split('-') : [];
	var to_int_array = [];
	for (var i = 0; i < to_array.length; i++) {
		to_int_array[i] = parseInt(to_array[i], 10);
	}
	var to_time = new Date(to_int_array[0], to_int_array[1] - 1,
			to_int_array[2], 23, 59, 59);

	return {
		'start_time' : from_time.format('yyyy-MM-dd hh:mm:ss'),
		'end_time' : to_time.format('yyyy-MM-dd hh:mm:ss')
	}
};
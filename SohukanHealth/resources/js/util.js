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
					if (jsonData.success == true) {
						callback(jsonData);
					} else {
						alert('failed', "info:" + jsonData.info + " ,code:"
										+ jsonData.code);
					}
				},
				error : function(XMLHttpRequest, textStatus, errorThrown) {
					alert('没有响应', '服务器没有响应');
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

function clearElement(element){
	var child_nodes = element.childNodes;

	if (child_nodes) {
		for (var i = 0; i < child_nodes.length; i++) {
			element.removeChild(child_nodes[i]);
		}
	}
};

// ------------------

var chart_date_handler = function(time_str) {
	time = new Date(time_str);
	return time.format('MM.dd hh:mm');
};
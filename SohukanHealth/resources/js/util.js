var myAjax = function(url, params, callback) {
	$.ajax({
		url : url,
		type : 'get',
		data : params,
		timeout : 10000,
		async : false,
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

var get_statistics_data = function(name) {
	url = '/statistics/' + name
	myAjax(url, null, function(obj) {
		data = obj.list;
	});
	return data;
};

var get_monitor_data = function(name) {
	url = '/monitor/' + name
	myAjax(url, null, function(obj) {
		data = obj.list;
	});
	return data;
};
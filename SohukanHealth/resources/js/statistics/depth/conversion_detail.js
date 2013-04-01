var make_conversion_chart = function(chartData) {
	var e = document.getElementById('depth_conversion')
	clearElement(e);

	// SERIAL CHART
	chart = new AmCharts.AmSerialChart();
	chart.dataProvider = chartData;
	chart.categoryField = "convert";
	chart.startDuration = 1;
	chart.addTitle('转化率', 20);

	// AXES
	// category
	var categoryAxis = chart.categoryAxis;
	categoryAxis.labelRotation = 90;
	categoryAxis.gridPosition = "start";

	// GRAPH
	var graph = new AmCharts.AmGraph();
	graph.valueField = "rate";
	graph.balloonText = "[[category]]: [[value]]";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 0.8;
	chart.addGraph(graph);

	chart.write(e.getAttribute('id'));
};

function strToDate(str){
    var arr = new Array();
    str = str.substr(0, 10)
    arr = str.split('-');
    var date = new Date(arr[0], arr[1] - 1, arr[2]);
    return date
}

var load_conversion = function(params, callback) {
	url = '/statistics/depth/conversion';

	var now = new Date();
	var to = $("#depth_conversion_to").val();
	to = to || now.format('yyyy-MM-dd hh:mm:ss');
	
    var from = $("#depth_conversion_from").val();
	tmp = strToDate(to)
    tmp.setDate(now.getDate() - 1)
	from = from || tmp.format('yyyy-MM-dd hh:mm:ss');

	var date_range = get_date_range(to, to);
	var size = $("#table_conversion #size").val();

	var params = {
		start_time : date_range.start_time,
		end_time : date_range.end_time,
		size : size
	};

	var e = document.getElementById('depth_conversion')
	clearElement(e);
	var loading = document.createElement('p')
	var loading_text = document.createTextNode('数据加载中...')
	loading.appendChild(loading_text);
	e.appendChild(loading);

	myAjax(url, params, function(obj) {
				data = obj;
				len = data.length;
				make_conversion_chart(data);
				prepare_conversion.data = data;

				if (callback && typeof callback == 'function') {
					callback();
				}
				$("#depth_conversion_from").val(from.substr(0, 10));
				$("#depth_conversion_to").val(to.substr(0, 10));
			});
};

var prepare_conversion = function() {
	$("#depth_conversion_from").datepicker({
				changeMonth : true,
				numberOfMonths : 2,
				dateFormat : "yy-mm-dd"
			});
	$("#depth_conversion_to").datepicker({
				changeMonth : true,
				numberOfMonths : 2,
				dateFormat : "yy-mm-dd"
			});
	$("#table_conversion #conversion_submit").click(load_conversion);
	$("#table_conversion #reset").click(function() {
				$("#depth_conversion_from").val('');
				$("#depth_conversion_to").val('');
			});

	$("#conversion_raw_data").click(function() {
		var now = new Date();
		var to = $("#depth_conversion_to").val();
		to = to || now.format('yyyy-MM-dd hh:mm:ss');

		var from = $("#depth_conversion_from").val();
		tmp = now;
		tmp.setDate(now.getDate() - 1)
		from = from || tmp.format('yyyy-MM-dd hh:mm:ss');

		var date_range = get_date_range(to, to);
		var size = $("#table_conversion #size").val();

		var url = "/statistics/depth/conversion?start_time="
				+ date_range.start_time + "&end_time=" + date_range.end_time
				+ "&size=" + size;
		window.open(url);
		return false;
	});
	/*
	 * $("#conversion_raw_data").click(function() { if
	 * (prepare_conversion.data) { // 数据表格 var data =
	 * prepare_conversion.data;
	 * 
	 * $('#box').empty().append('<div class="clearfix"></div>');
	 * 
	 * var table_count = data.length > 150 ? 5 : data.length / 30; var url_table =
	 * document.createElement('table') url_table.style.fontSize = '11px';
	 * url_table.style.width = '900px'; url_table.style.wordBreak = 'break-all';
	 * 
	 * urls = data[index].urls; var len = urls.length >= 100 ? 100 :
	 * urls.length;
	 * 
	 * for (var k = 0; k < len; k++) { var tr = document.createElement('tr');
	 * for (var l = 0; l < 3; l++, k++) { if (urls[k]) { var td =
	 * document.createElement('td'); td.style.width = '450px';
	 * td.style.textAlign = 'left'; var a = document.createElement('a');
	 * a.setAttribute('href', urls[k]); a.target = "_blank"; var a_text =
	 * document.createTextNode(urls[k]); a.appendChild(a_text);
	 * td.appendChild(a); tr.appendChild(td); } } k--;
	 * url_table.appendChild(tr); } $('#box div').append(table);
	 * 
	 * $.blockUI({ message : $('#box'), css : { top : '20%', left : '30%',
	 * textAlign : 'left', marginLeft : '-320px', marginTop : '-145px',
	 * background : 'none' } }); $('.blockOverlay').attr('title',
	 * '单击关闭').click($.unblockUI); } else { load_conversion(); } return
	 * false; });
	 */
	load_conversion();
};

$(document).ready(function() {
			prepare_conversion();
		});

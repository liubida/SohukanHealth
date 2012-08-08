var make_bookmark_website_for_user_chart = function(chartData) {
	var e = document.getElementById('depth_bookmark_website_for_user')
	clearElement(e);

	// SERIAL CHART
	chart = new AmCharts.AmSerialChart();
	chart.dataProvider = chartData;
	chart.categoryField = "domain";
	chart.startDuration = 1;
	chart.addTitle('文章来源网站(UV)', 20);

	// AXES
	// category
	var categoryAxis = chart.categoryAxis;
	categoryAxis.labelRotation = 90;
	categoryAxis.gridPosition = "start";

	// GRAPH
	var graph = new AmCharts.AmGraph();
	graph.valueField = "count";
	graph.balloonText = "[[category]]: [[value]]";
	graph.type = "column";
	graph.lineAlpha = 0;
	graph.fillAlphas = 0.8;
	chart.addGraph(graph);

	chart.write(e.getAttribute('id'));
};

var load_bookmark_website_for_user = function(params, callback) {
	url = '/statistics/depth/bookmark_website_for_user';

	var from = $("#depth_bookmark_website_for_user_from").val();
	var to = $("#depth_bookmark_website_for_user_to").val();

	var date_range = get_date_range(from, to);
	var size = $("#table_bookmark_website_for_user #size").val();
	var radio_type = parseInt(
			$("#table_bookmark_website_for_user :radio:checked").val(), 10);

	var params = {
		start_time : date_range.start_time,
		end_time : date_range.end_time,
		size : size
	};

	var e = document.getElementById('depth_bookmark_website_for_user')
	clearElement(e);
	var loading = document.createElement('p')
	var loading_text = document.createTextNode('数据加载中...')
	loading.appendChild(loading_text);
	e.appendChild(loading);

	myAjax(url, params, function(obj) {
				data = obj.list;
				len = data.length;
				make_bookmark_website_for_user_chart(data);
				prepare_bookmark_website_for_user.data = data;

				if (callback && typeof callback == 'function') {
					callback();
				}
			});
};

var prepare_bookmark_website_for_user = function() {
	$("#depth_bookmark_website_for_user_from").datepicker({
		changeMonth : true,
		numberOfMonths : 2,
		dateFormat : "yy-mm-dd",
		onSelect : function(selectedDate) {
			$("#depth_bookmark_website_for_user_to").datepicker("option",
					"minDate", selectedDate);
		}
	});
	$("#depth_bookmark_website_for_user_to").datepicker({
				changeMonth : true,
				numberOfMonths : 2,
				dateFormat : "yy-mm-dd"
			});
	$("#bookmark_website_for_user_raw_data").click(function() {
				if (prepare_bookmark_website_for_user.data) {
					// 数据表格
					var data = prepare_bookmark_website_for_user.data;

					$('#box').empty().append('<div class="clearfix"></div>');
					var table_count = data.length > 150 ? 5 : data.length / 30;
					for (var j = 0; j < table_count; j++) {
						var table = document.createElement('table')
						table.style.fontSize = '12px';
						table.style.float = 'left';
						var th0 = document.createElement('th')
						var th0_text = document.createTextNode("序号");
						th0.appendChild(th0_text);
						var th1 = document.createElement('th')
						var th1_text = document.createTextNode("网站");
						th1.appendChild(th1_text);
						var th2 = document.createElement('th')
						var th2_text = document.createTextNode("用户数");
						th2.appendChild(th2_text);

						table.appendChild(th0);
						table.appendChild(th1);
						table.appendChild(th2);

						var index = 0;
						for (var i = 0; i < 30; i++) {
							var tr = document.createElement('tr');
							index = j * 30 + i;
							if (index >= data.length)
								break;

							// 序号列
							var td = document.createElement('td');
							var td_text = document.createTextNode(index + 1);
							td.appendChild(td_text);
							tr.appendChild(td);

							// 网站列
							var td = document.createElement('td');
							var td_text = document
									.createTextNode(data[index].domain);
							td.appendChild(td_text);
							tr.appendChild(td);

							// 用户数
							var td = document.createElement('td');
							var td_text = document
									.createTextNode(data[index].count);
							td.appendChild(td_text);
							tr.appendChild(td);

							table.appendChild(tr);
						}
						$('#box div').append(table);
					}

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
				} else {
					load_bookmark_website_for_user();
				}
				return false;
			});
	$("#table_bookmark_website_for_user #submit")
			.click(load_bookmark_website_for_user);
	$("#table_bookmark_website_for_user #reset").click(function() {
				$("#depth_bookmark_website_for_user_from").val('');
				$("#depth_bookmark_website_for_user_to").val('');
			});

	load_bookmark_website_for_user();
};

$(document).ready(function() {
			prepare_bookmark_website_for_user();
		});
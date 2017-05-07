

function readURL(input, id) {
	if(input.files && input.files[0]) {

		var reader = new FileReader();
		reader.onload = function(e) {
			$('#' + id).attr('src', e.target.result).width(350).height(350);
		};

		reader.readAsDataURL(input.files[0]);

	};
}

function selections() {
	var lst = [];

	$('.list-vals').find('option').not(':first').each(function() {
		
		if($(this).is(':checked')) {
			lst.push($(this).text());
		}
	});

	return lst;
}

function ajaxPostCall(url, data, callback) {

	console.log(url);
	console.log(data);

	$.ajaxQueue({
		url: url,
		type: 'POST',
		cache: false,
		data: JSON.stringify(data),
		contentType: 'application/json;charset=UTF-8',
		success: function(resp) {
			console.log(resp);
			callback($.parseJSON(resp));
		},
		error: function(errXqhr, errtext, errcode) {
			alert(errtext);
		}
	});

}

function ajaxPostCall2(url, data, callback, thisRow) {

	console.log(url);
	console.log(data);

	$.ajaxQueue({
		url: url,
		type: 'POST',
		cache: false,
		data: JSON.stringify(data),
		contentType: 'application/json;charset=UTF-8',
		success: function(resp) {
			console.log(resp);
			callback($.parseJSON(resp), thisRow);
		},
		error: function(errXqhr, errtext, errcode) {
			alert(errtext);
		}
	});

}

function createTabHeaders(headers) {

	var appndString = "";

	var numCols = Math.ceil(12 / headers.length);
	console.log(numCols);

	for(var i = 0; i < headers.length; i++) {
		appndString +="<li class='tab col s" + String(numCols) +"'><a href='#record" + String(i+1) + "'>" + headers[i] + "</a></li>";
	}

	var finalString = "<div class='col s12'>"+ 
						"<ul class='tabs'>" +
							appndString +
						"</ul>" +
					  "</div>";

	console.log(finalString);

	$('#all-tabs').children().remove();
	$('#all-tabs').append(finalString);

	return "done"
}

function getStudentList() {

	// Get all the classes selected
	var sels = selections();

	// url for akax request
	path = '/sendNotice/getStudentList';
	data = {'classes' : sels};

	console.log(data);

	// ajax call
	var studList = ajaxPostCall(path, data, studentsToTable);


}

function getFacultyList() {

	// Get all the classes selected
	// var sels = selections();

	// url for akax request
	path = '/sendNotice/getFacultyList';
	data = {'group' : ['faculty']};

	console.log(data);

	// ajax call
	var facsList = ajaxPostCall(path, data, facultyToTable);


}

function studentsToTable(tableInfo) {
	$('#all-tabs').children().remove();

	var studentsTable = "<table class='bordered highlight centered notice-recpnts'><thead>"+
							"<tr>"+
								"<th>"+
									"S.No."+
								"</th>"+
								"<th>"+
									"Roll Number"+
								"</th>"+								
								"<th>"+
									"First Name"+
								"</th>"+
								"<th>"+
									"Middle Name"+
								"</th>"+
								"<th>"+
									"Last Name"+
								"</th>"+
								"<th>"+
									"Class"+
								"</th>"+
								"<th>"+
									"Gender"+
								"</th>"+
								"<th>"+
									"Primary Contact"+
								"</th>"+
								"<th>"+
									"Notice Sent ?"+
								"</th>"+																																																			
							"</tr>"+
						"</thead><tbody><tr></tr></tbody></table>";
	$('#all-tabs').append(studentsTable);

	for (var key in tableInfo) {
		
		var classrow = "<tr>"+
							"<td> Class : " + key + "</td>"+
						"</tr>";

		$('#all-tabs tr:last').after(classrow);

		for (var i=0; i<tableInfo[key].length; i++) {
			var temprow = "<tr>"+
							"<td>" + (parseInt(i) + 1) + "</td>"+
							"<td>" + tableInfo[key][i][0] + "</td>"+
							"<td>" + tableInfo[key][i][1] + "</td>"+
							"<td>" + tableInfo[key][i][2] + "</td>"+
							"<td>" + tableInfo[key][i][3] + "</td>"+
							"<td>" + tableInfo[key][i][4] + "</td>"+
							"<td>" + tableInfo[key][i][5] + "</td>"+
							"<td name='mob-nmbr'>" + tableInfo[key][i][6] + "</td>"+
							"<td name='send-sts'></td>"+
						  "</tr>";
			$('#all-tabs tr:last').after(temprow);

		}


	}
}

function facultyToTable(tableInfo) {
	$('#all-tabs').children().remove();

	var facsTable = "<table class='bordered highlight centered notice-recpnts'><thead>"+
							"<tr>"+
								"<th>"+
									"S.No."+
								"</th>"+
								"<th>"+
									"ID Number"+
								"</th>"+								
								"<th>"+
									"Full Name"+
								"</th>"+
								"<th>"+
									"Gender"+
								"</th>"+
								"<th>"+
									"Primary Contact"+
								"</th>"+	
								"<th>"+
									"Notice Sent ?"+
								"</th>"+																																											
							"</tr>"+
						"</thead><tbody><tr></tr></tbody></table>";
	$('#all-tabs').append(facsTable);

	for (var key in tableInfo) {
		
		// var classrow = "<tr>"+
		// 					"<td> Class : " + key + "</td>"+
		// 				"</tr>";

		// $('#all-tabs tr:last').after(classrow);

		for (var i=0; i<tableInfo[key].length; i++) {
			var temprow = "<tr>"+
							"<td>" + (parseInt(i) + 1) + "</td>"+
							"<td>" + tableInfo[key][i][0] + "</td>"+
							"<td>" + tableInfo[key][i][1] + "</td>"+
							"<td>" + tableInfo[key][i][2] + "</td>"+
							"<td name='mob-nmbr'>" + tableInfo[key][i][3] + "</td>"+
							"<td name='send-sts'></td>"+
						  "</tr>";
			$('#all-tabs tr:last').after(temprow);

		}


	}
}

function sendNoticeAll() {

	var $rows = $('table.notice-recpnts > tbody > tr');
	var msg = $('.notice').val();
	// alert(msg);

	$rows.not(':first').each(function() {

		var x = $(this).find('[name=mob-nmbr]').text();
		var data = {'msg' : msg, 'number' : x};

		path = '/sendNotice/sendTextAll'

		if (x != "") {
			var tempMsgResp = ajaxPostCall2(path, data, noticeResp, $(this));
		}

	});


}

function noticeResp(resp, thisRow) {
	thisRow.find('[name=send-sts]').text(resp);
}

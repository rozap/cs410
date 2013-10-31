var Home = function() {
	attachTo.call(this, '.home-action');

	this.submitRepo = function(e) {
		var url = $('#repo-url').val(),
			$res = $('#submit-result');
		console.log(url);
		$.ajax({
			url: '/api/repos',
			data: JSON.stringify({
				csrftoken: tok,
				url: url
			}),
			type: 'POST',
			dataType: 'json',
			contentType: 'json',

		}).then(function(data) {
			$res.removeClass('alert-danger').addClass('alert-success').html(data.message).show();
		}, function(resp) {
			var data = JSON.parse(resp.responseText);
			$res.addClass('alert-danger').removeClass('alert-success').html(data.message).show();
		});
		console.log("Submit!");
	}


};
var Drawer = function(repoId) {

	var functionResp;
	var interactionResp;

	var onReady = _.after(2, function() {
		var globe = new DAT.Globe($('#globe')[0]);

		var points = [],
			uPoints = _.uniq(functionResp, function(p) {
				return p.commit.actor.lat + p.commit.actor.lng
			});
		// console.log(uPoints);

		_.each(functionResp, function(p) {
			points.push(Math.round(p.commit.actor.lat));
			points.push(Math.round(p.commit.actor.lng));
			points.push(.8);
		});

		globe.addData(points, {
			format: 'magnitude',
			name: 'foo',
			animated: true
		});



		globe.createPoints();

		_.each(interactionResp, function(interaction) {

			if (interaction.caller.commit.actor.lat != interaction.callee.commit.actor.lat) {
				console.log("Different!");
			}

			globe.addLine(
				interaction.caller.commit.actor.lat, interaction.caller.commit.actor.lng,
				interaction.callee.commit.actor.lat, interaction.callee.commit.actor.lng
			);
		});

		globe.animate();

	});


	$.getJSON('/api/repos/' + repoId).success(function(resp) {
		functionResp = resp;
		onReady();
	});
	$.getJSON('/api/repos/' + repoId + '/interactions').success(function(resp) {
		interactionResp = resp;
		onReady();
	})

};
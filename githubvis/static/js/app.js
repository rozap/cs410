var Drawer = function(repoId) {

	var actorsResp;
	var functionResp;
	var interactionResp;
	var filesResp;
	var globe;

	var fileLines = [];
	var functionLines = [];

	var showFunctions = true;
	var showFiles = true;


	attachTo.call(this, '.toggle-functions');
	attachTo.call(this, '.toggle-files');


	var init = function() {
		globe = new DAT.Globe($('#globe')[0]);
	}


	var addActors = function() {
		if (!actorsResp) {
			return;
		}


		var points = [],
			uPoints = _.uniq(actorsResp, function(p) {
				return p.commit.actor.lat + p.commit.actor.lng
			});
		// console.log(uPoints);

		_.each(actorsResp, function(p) {
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

		globe.animate();

	}



	var addFunctionCalls = function() {
		if (!interactionResp) {
			return;
		}
		_.each(interactionResp, function(interaction) {
			functionLines.push(globe.addLine(
				interaction.caller.commit.actor.lat, interaction.caller.commit.actor.lng,
				interaction.callee.commit.actor.lat, interaction.callee.commit.actor.lng, 0x00ff00
			));
		});
		globe.createPoints();

	}

	var addFiles = function() {
		if (!filesResp) {
			return;
		}
		_.each(filesResp, function(fchange) {
			fileLines.push(globe.addLine(
				fchange.change1.actor.lat, fchange.change1.actor.lng,
				fchange.change2.actor.lat, fchange.change2.actor.lng, 0x0000ff, .7
			));
		});
		globe.createPoints();

	}


	this.toggleFunctions = function(e) {
		showFunctions = !showFunctions;
		_.each(functionLines, function(line) {
			line.visible = showFunctions;
		});
	};
	this.toggleFiles = function(e) {
		showFiles = !showFiles;
		_.each(fileLines, function(line) {
			line.visible = showFiles;
		});
	};

	init();


	$.getJSON('/api/repos/' + repoId).success(function(resp) {
		actorsResp = resp;
		addActors();
	});
	$.getJSON('/api/repos/' + repoId + '/interactions').success(function(resp) {
		interactionResp = resp;
		addFunctionCalls();
	});
	$.getJSON('/api/repos/' + repoId + '/common_file_changes').success(function(resp) {
		filesResp = resp;
		addFiles();
	});



};
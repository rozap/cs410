var Drawer = function(repoId) {

	$.getJSON('/api/repos/' + repoId).success(function(resp) {
		var globe = new DAT.Globe($('#globe')[0]);

		var points = [],
			uPoints = _.uniq(resp, function(p) {
				return p.commit.actor.lat + p.commit.actor.lng
			});
		// console.log(uPoints);

		_.each(resp, function(p) {
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

	});

};



$(document).ready(function() {

	if (!window.requestAnimationFrame) {

		window.requestAnimationFrame = (function() {

			return window.webkitRequestAnimationFrame ||
				window.mozRequestAnimationFrame ||
				window.oRequestAnimationFrame ||
				window.msRequestAnimationFrame ||
				function( /* function FrameRequestCallback */ callback, /* DOMElement Element */ element) {

					window.setTimeout(callback, 1000 / 60);

			};

		})();

	}
});
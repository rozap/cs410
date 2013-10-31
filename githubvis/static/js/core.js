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


(function() {

	window.attachTo = function(el, ev) {
		ev = ev || 'click';
		var that = this;
		$(el).on('click', function(e) {
			var action = $(e.currentTarget).data('action');
			that[action].call(that, e);
		});
	}

})();
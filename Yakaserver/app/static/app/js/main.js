$(document).ready(function() {

  $("div.blog-post").hover(
    function() {
        $(this).find("div.content-hide").slideToggle("fast");
    },
    function() {
        $(this).find("div.content-hide").slideToggle("fast");
    }
  );

  $('.flexslider').flexslider({
		prevText: '',
		nextText: ''
	});

  $('.testimonails-slider').flexslider({
    animation: 'slide',
    slideshowSpeed: 5000,
    prevText: '',
    nextText: '',
    controlNav: false
  });

  $(function(){

  // Instantiate MixItUp:

  $('#Container').mixItUp();

  $(document).ready(function() {
      $(".fancybox").fancybox();
    });
  });

	// Atelier inscription
	var atelierPlaceForm = $(".atelier-total-form");

	if (atelierPlaceForm) {
		new PriceUpdateOnSeatChange(atelierPlaceForm);
	}

	$('[data-toggle="datepicker"]').datepicker();
});


// Atelier inscription, get number of seat & calculate the total price
var PriceUpdateOnSeatChange = function(formTarget) {
	this.form = formTarget;
	this.seatInput = this.form.find(".atelier-place-input");
	this.seatText = this.form.find(".atelier-place");
	this.totalText = this.form.find(".atelier-total");
	this.priceSpan = this.form.find(".atelier-price").text();
	this.price = parseFloat(this.priceSpan);

	this.defaultText();
	this.initEvents();
}

PriceUpdateOnSeatChange.prototype.initEvents = function () {
	var _ = this;

	this.seatInput.on("change", function() {
		var seatNumber = _.seatInput.val();

		_.changeText(seatNumber);
	});
};

PriceUpdateOnSeatChange.prototype.changeText = function (seatNumber) {
	this.seatText.html(seatNumber);

	var total = seatNumber * this.price;

	this.totalText.html(total);
// if totalpremium.exist
	// FIXME -10% premium
};

PriceUpdateOnSeatChange.prototype.defaultText = function () {
	this.totalText.html(this.price);
};

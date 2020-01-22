// JavaScript Document


(function($) {
  jQuery(document).ready(function() {

    $('.mobile-nav-btn').click(function() {
    	if( $('nav').hasClass('active-nav') ) {
	      $('.mobile-nav-container').toggleClass('active-nav');
	      $('.mobile-nav-btn').toggleClass('active-nav');
	      $('nav').toggleClass('active-nav');
    		$('nav li').removeClass('show-nav');

	      // Remove Page Crop
	      setTimeout(function(){
        $('.page-wrap').removeClass('crop'); // release the "proper" crop
        $('.page-wrap').height('auto'); // resets height for scolling
      	}, 300);

    	} else {
    		$('.page-wrap').addClass('crop'); // "proper" crop
	      $('.mobile-nav-btn').toggleClass('active-nav');
	      $('.mobile-nav-container').toggleClass('active-nav');
	      $('nav').toggleClass('active-nav');
	      
        
	      // Show me the links
	      var timer = 0;
	      $.each($('nav li'), function (i, s) {
	        timer = 300 * i;
	        setTimeout(function () {
	          $(s).addClass('show-nav');
	        }, timer); // show menu items on timer
	      });
      	
	    }
    });

  });

}(jQuery));
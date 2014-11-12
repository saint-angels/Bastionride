jQuery(document).ready(function() {

    var current;
    var img_urls = [];
    var body = $('body');
    var lightbox;

	$('.lightbox_trigger').click(function(e) {

		e.preventDefault();
		//Get clicked link href
        var image_href = this.href;

        // determine the index of clicked trigger
        current = $('.lightbox_trigger').index(this);

		if (lightbox && lightbox.length > 0) { // #lightbox exists
    	    $('#lightbox_content').html('<img src="' + image_href + '" />');
			lightbox.fadeIn(300);
		}
		else {
            var lightboxHtml =
                '<div id="lightbox">' +
                    '<p>Click to close</p>' +
                    '<div id="lightbox_content">' +
                        '<img src="' + image_href +'" />' +
                    '</div>' +
                    '<ul id="help_block"><li>Use arrows to navigate</li><li>Click anywhere to exit gallery</li></ul>' +
                '</div>';

            body.append(lightboxHtml);

            $('#imageSet').find('.lightbox_trigger').each(function() {
            var $href = $(this).attr('href');
                img_urls.push($href);
            });
            lightbox = $('#lightbox');
		}

//        $([img_urls[current]]).preload();
        $('#help_block').hide();
	});


    $.fn.closeLightBox = function(e) {
        e.preventDefault();
        e.stopPropagation();
        lightbox.fadeOut(300);
    }

    $.fn.toggleHelpBlock = function(e) {
        pde(e);
        e.stopPropagation();
        $('#help_block').toggle();
    }

    function pde(e)//Function to prevent Default Events
    {
        if(e.preventDefault)
            e.preventDefault();
        else
            e.returnValue = false;
    }

    $.fn.Next= function(e) {
        e.preventDefault();
        e.stopPropagation();

        $('#help_block').hide();

        $('#lightbox_content').html("<img src=\"/static/mainapp/images/ajax-loader.gif\" />");

        var dest = current != img_urls.length - 1 ? current + 1 : 0;

        $.ajax({
            type: "GET",
            url: img_urls[dest],
            success: function (d) {
                // replace div's content with returned data
                $('#lightbox_content').html('<img src="' + img_urls[dest] + '" />');
                // setTimeout added to show loading
//                setTimeout(function () {
//                    $('#lightbox_content').html('<img src="' + img_urls[dest] + '" />');
//                }, 2000);
            }
        });
        current = dest;
    }

    $.fn.Previous= function(e) {
        e.preventDefault();
        e.stopPropagation();
        $('#help_block').hide();
        $('#lightbox_content').html('<img src="/static/mainapp/images/ajax-loader.gif" />');

        var dest = current != 0 ? current - 1 : img_urls.length - 1;

        $.ajax({
            type: "GET",
            url: img_urls[dest],
            success: function () { $('#lightbox_content').html('<img src="' + img_urls[dest] + '" />'); }
        });
        current = dest;
    }


    body.on('click', '#lightbox', function(e) {
       $.fn.closeLightBox(e);
    });

    body.on('keydown',function(e){
      switch (e.which) {
          case 27:
              $.fn.closeLightBox(e);
          break;
//          case 116:
//             e.preventDefault();
//          break;
          case 39:
            $.fn.Next(e);
          break;
          case 37:
            $.fn.Previous(e);
          break;
          case 112:
            $.fn.toggleHelpBlock(e);
      }
    });

     $.fn.preload = function() {
        this.each(function(){
            $('<img/>')[0].src = this;
        });
    }
});
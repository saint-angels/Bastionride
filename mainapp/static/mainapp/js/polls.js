jQuery(document).ready(function() {

    $.fn.updatePollInfoImg = function(img) {
      var img_url_parts = img.attr('src').split('/');
      var img_idx = img_url_parts.pop();
      $.ajax({
            type: "GET",
            url: img_url_parts.join('/') + '_b64/' + img_idx,
            processData : false,
            success: function(b64data)
            {
                img.attr("src", "data:image/png;base64," + b64data);
            }
        });
    };

    $.fn.updateAllPollInfoImages = function() {
        $("img[id^=question_info_image_]").each(function(){
            var src = $(this).attr('src');
            $(this).attr('src', src);
//             $.fn.updatePollInfoImg($(this));
          });
    };

    $.fn.post_vote_form = function(vote_form) {
        $.ajax({
            type: "POST",
            url: vote_form.attr('action'),
            data: vote_form.serialize(), // serializes the form's elements.
            success: function(json)
            {
                if (json['status'] == 1) {
                    vote_form.find('img.captcha').attr('src', json['new_cptch_image']);
                    vote_form.find('input#id_captcha_0').attr('value', json['new_cptch_key']);
                    vote_form.find('input#id_captcha_1').val('');
                }
                else {

                }

                $.fn.updateAllPollInfoImages();
            }
        });
    };

    setInterval(function() {
        $.fn.updateAllPollInfoImages();
    }, 10000);


    $('form').each(function(){
      $(this).submit(function(event) {
        event.preventDefault();
        console.log("form submitted!");
        $.fn.post_vote_form($(this));
      });
    });



    //CSRF FIX FOR AJAX

    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
});



});
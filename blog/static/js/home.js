  $(document).ready(function(event) {
      $(document).on('click', '.updateButton' , function(event) {
        event.preventDefault();
              $('#loading').show();
              $('#post_display').hide();
          var member_id = $(this).attr('member_id');
          var csrf = $(this).attr('csrf');
          $.ajax({
            type: "POST",
            url: "{% url 'blog-home' %}",
            data : { 'id':member_id, 'csrfmiddlewaretoken': csrf, 'action' : "View_Post"},
            dataType: 'json',
            success : function(response) {
              $('#post_display').html(response['form']);
              $('#loading').hide();
              $('#post_display').show();
              console.log("success");
            },
            error : function(rs, e) {
              $('#post_display').html("an error occured");
              console.log(rs.responseText);
            }
          });
      });
  });

  $(document).ready(function(event) {
      $(document).on('click', '.homeLikeButton' , function(event) {
        event.preventDefault();
        event.stopImmediatePropagation();
          var member_id = $(this).attr('member_id');
          $.ajax({
            type: "POST",
            url: "{% url 'blog-home' %}",
            data : { 'id':member_id, 'csrfmiddlewaretoken': '{{csrf_token}}', 'action' : "Like_Feed"},
            dataType: 'json',
            success : function(response) {
              $('#feed_display').html(response['form']);
              console.log("success");
            },
            error : function(rs, e) {
              $('#feed_display').html(response['main']);
              $('#post_display').html("an error occured");
              console.log(rs.responseText);
            }
          });
      });
  });

  $(document).ready(function(event) {
      $(document).on('click', '.newPostButton' , function(event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        var member_id = $(this).attr('member_id');
          $.ajax({
            type: "POST",
            url: "{% url 'blog-home' %}",
            data : { 'id':member_id,'csrfmiddlewaretoken': '{{csrf_token}}', 'action' : "New_Post"},
            dataType: 'json',
            success : function(response) {
              $('#feed_display').html(response['form']);
              console.log("success");
            },
            error : function(rs, e) {
              console.log(rs.responseText);
            }
          });
      });

  });

  $(document).ready(function(event) {
      $(document).on('hidden', '#newPostModalCenter' , function(event) {
                    console.log("CLOSE MODAL");
      });

  });

  function getCookie(c_name)
  {
      if (document.cookie.length > 0)
      {
          c_start = document.cookie.indexOf(c_name + "=");
          if (c_start != -1)
          {
              c_start = c_start + c_name.length + 1;
              c_end = document.cookie.indexOf(";", c_start);
              if (c_end == -1) c_end = document.cookie.length;
              return unescape(document.cookie.substring(c_start,c_end));
          }
      }
      return "";
   }

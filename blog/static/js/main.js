  $(document).ready(function() {

      $(document).on('click', '.updateButton' , function() {

          var member_id = $(this).attr('member_id');
          var name = "pol"
          req = $.ajax({
              url : '/view',
              type : 'POST',
              data : { name : name, id : member_id }
          });

          req.done(function(data) {

              $('#post_replacer').fadeOut(1000).fadeIn(1000);
              $('#post_replacer').html("pola");

          });


      });

  });

  //This is the next Jquery

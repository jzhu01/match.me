$(document).ready(function () {

  $("#btn-submit").click(function (e) {
    e.preventDefault();
    // get solo hacker's list of skills
    var likes = [];

    var user_name = $("#user_name").val();
    var user_age = $("#user_age").val();
    var user_bio = $("#user_bio").val();
    var user_img_link = "http://www.freelanceme.net/Images/default%20profile%20picture.png";
    if ($("#user_img_link").val()) {
      var user_img_link = $("#user_img_link").val();
    }
    var user_gender;


    $(".user_gender").each( function () {
      if ($(this).is(":selected")) {
        user_gender = $(this).val();
      }
    });

    $(".user_like").each( function() {
      if ($(this).is(":selected")) {
        var interest = $(this).val();
        likes.push(interest);
      }
      console.log(likes);
      console.log('stringify');
      console.log(JSON.stringify(likes));
    });


    $.ajax({ method: "post",
             url: "/saveuserinput",
            //  url: "/groupinput",
             data: { user_name : user_name,
                    user_age : user_age,
                    user_img_link : user_img_link,
                    user_bio: user_bio,
                    user_gender: user_gender,
                    likes : JSON.stringify(likes) }
    }).done( function(data) {
      console.log("AJAX finished.");
      // location.href = "http://www.example.com/ThankYou.html"
      location.href = "/matches";
    });

  });

});

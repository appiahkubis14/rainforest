$('input[type="submit"]').click(function(e){

 e.preventDefault();
    if ($("#addform")[0].checkValidity() == true) {
        // Code goes here
        // var fname = $("#firstname").val();
        // var lname = $("#lastname").val();
        var uname = $("#username").val();
        var password = $("#password").val();
        $.ajax({
            url: "/loginauthenticate/",
            type: "POST",
            data: { "username": uname, "password": password },
            dataType: "",
            async: false,
            success: function(data) {
                console.log(data)
                if (data == "pass") {
                   
                   $('.login').addClass('test')
                    setTimeout(function(){
                      $('.login').addClass('testtwo')
                    },300);
                    setTimeout(function(){
                      $(".authent").show().animate({right:-320},{easing : 'easeOutQuint' ,duration: 600, queue: false });
                      $(".authent").animate({opacity: 1},{duration: 200, queue: false }).addClass('visible');
                    },500);
                    setTimeout(function(){
                      $(".authent").show().animate({right:90},{easing : 'easeOutQuint' ,duration: 600, queue: false });
                      $(".authent").animate({opacity: 0},{duration: 200, queue: false }).addClass('visible');
                      $('.login').removeClass('testtwo')
                    },2500);
                    setTimeout(function(){
                      $('.login').removeClass('test')
                      $('.login div').fadeOut(123);
                    },2800);
                    setTimeout(function(){
                      $('.success').fadeIn();
                    },3200);
                    setTimeout(function(){
                      window.location.replace(/dashboard/)
                    },3400);

                } else if (data == "exists") {
                  alert(data)
                    // notification(data["status"], "notify");
                } else if (data == "fail") {
                  alert(data)
                    // notification(data["status"], "notify");
                }
            }
        });
    } else {
        $("#addform").valid();
    }

  // $('.login').addClass('test')
  // setTimeout(function(){
  //   $('.login').addClass('testtwo')
  // },300);
  // setTimeout(function(){
  //   $(".authent").show().animate({right:-320},{easing : 'easeOutQuint' ,duration: 600, queue: false });
  //   $(".authent").animate({opacity: 1},{duration: 200, queue: false }).addClass('visible');
  // },500);
  // setTimeout(function(){
  //   $(".authent").show().animate({right:90},{easing : 'easeOutQuint' ,duration: 600, queue: false });
  //   $(".authent").animate({opacity: 0},{duration: 200, queue: false }).addClass('visible');
  //   $('.login').removeClass('testtwo')
  // },2500);
  // setTimeout(function(){
  //   $('.login').removeClass('test')
  //   $('.login div').fadeOut(123);
  // },2800);
  // setTimeout(function(){
  //   $('.success').fadeIn();
  // },3200);





});

$('input[type="text"],input[type="password"]').focus(function(){
  $(this).prev().animate({'opacity':'1'},200)
});
$('input[type="text"],input[type="password"]').blur(function(){
  $(this).prev().animate({'opacity':'.5'},200)
});

$('input[type="text"],input[type="password"]').keyup(function(){
  if(!$(this).val() == ''){
    $(this).next().animate({'opacity':'1','right' : '30'},200)
  } else {
    $(this).next().animate({'opacity':'0','right' : '20'},200)
  }
});

var open = 0;
$('.tab').click(function(){
  $(this).fadeOut(200,function(){
    $(this).parent().animate({'left':'0'})
  });
});




// $("#submit").click(function(e) {
//     e.preventDefault();
//     if ($("#addform")[0].checkValidity() == true) {
//         // Code goes here
//         var username = $("#username").val();
//         var password = $("#password").val();
//         $.ajax({
//             url: "/loginauthenticate/",
//             type: "POST",
//             data: {  "username": password, "username": password},
//             dataType: "json",
//             async: false,
//             success: function(data) {
//                 if (data["status"] == "pass") {
//                    alert(data["status"])
//                 } else if (data["status"] == "exists") {
//                    alert(data["status"])
//                 } else if (data["status"] == "fail") {
//                     alert(data["status"]);
//                 }
//             }
//         });
//     } else {
//         $("#addform").valid();
//     }
// });
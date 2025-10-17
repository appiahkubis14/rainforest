$('.top_header').on('click', '#signout', function(e) {
    e.preventDefault();
    window.location.href = "/logout/";
});
$('.top_header').on('click', '#changepassword', function(e) {
    e.preventDefault();
    $("#changepassword_modal").modal('show');
});
$("#chngpwd").on('click', function(e) {
    e.preventDefault();
    var oldpass = $("#oldpass").val();
    var newpass = $("#newpass").val();
    var repnewpass = $("#repnewpass").val();
    if ($("#changepassform")[0].checkValidity() == true && newpass == repnewpass) {
        $.ajax({
            url: "/changepassword/",
            type: "POST",
            data: { 'oldpass': oldpass, 'newpass': newpass, 'repnewpass': repnewpass },
            async: false,
            success: function(data) {
                notification(data, "notifypwd");
                if (data == "pass") {
                    submitForm("#editform");
                }
            }
        });
    } else {
        $("input:password").each(function() {
            $(this).valid();
        });
    }
});
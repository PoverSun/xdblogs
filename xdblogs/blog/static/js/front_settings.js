
//修改密码

$(function () {
    $('#reset-pwd-btn').click(function (event) {
        event.preventDefault();
        var dialog = $('#error-tips');
        var password_input = $('#password');
        var new_password_input = $('#new_password');
        var repeat_password_input = $('#repeat_password');
        var password = password_input.val();
        var new_password = new_password_input.val();
        var repeat_password = repeat_password_input.val();
        var tipTags = $('.modal-content>.modal-body');
        $.ajax({
            type:'POST',
            url: '/blog/front_reset_pwd/',
            data:{
                'password':password,
                'new_password':new_password,
                'repeat_password':repeat_password
            },
            success:function (result) {
                if(result['code']==200){
                    tipTags.children().text(result['message']);
                    password_input.val('');
                    new_password_input.val('');
                    repeat_password_input.val('');
                    $('.reload-btn').remove();
                    dialog.modal('show');
                }else{
                    //清除前面输入的
                    password_input.val('');
                    new_password_input.val('');
                    repeat_password_input.val('');
                    tipTags.children().text(result['message']);
                    dialog.modal('show');
                }
            },
            error:function (error) {
                console.log('error'+error);
                dialog.modal('show');
            },
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        });
    });
});


$(function () {
    $('.reload-btn').click(function () {
        console.log('sssssssss');
        $('#update-pwd').addClass('active');
        $('#articles').removeClass("active");
    });
})

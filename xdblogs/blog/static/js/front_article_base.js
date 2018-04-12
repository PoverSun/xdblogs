
//add_articles
$(function () {
    $('.submit-btn').click(function (event) {
        event.preventDefault();
        var input_title = $('#input-title');
        var input_subtitle = $('#input-subtitle');
        var input_category = $("#categorys").find("option:selected");
        var input_tags = $('input[name="tag"]:checked');
        var input_textarea = $('#input-textarea');
        var title = input_title.val();
        var subtitle = input_subtitle.val();
        var category = input_category.val();
        var tags=[];
        var textarea_content = input_textarea.val();
        input_tags.each(function () {
            tags.push($(this).val());
        });
        var dialog = $('#myModal');
        var url = window.location.href;
        $.ajax({
            type:'post',
            url: url,
            data: {
                'title':title,
                'subtitle':subtitle,
                'category':category,
                'tags[]':tags,
                'textarea_content':textarea_content
            },
            success:function (result) {
                if (result['code']==200){
                     input_title.val('');
                     input_textarea.val('');
                     input_subtitle.val('');
                     input_tags.removeAttr("checked");
                     dialog.modal('show');
                }else{
                    alert('出错！');
                }
            },
            error:function (error) {
                console.log('error'+error);
            },
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        });
    });
});
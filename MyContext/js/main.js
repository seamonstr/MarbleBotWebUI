(function (w){

    $('.cell').click(function () {
        var thiz = $(this)
          , tick = $('.tick')
          , val = thiz.data('value')
          , n = tick.length + 1;

        if(tick.length < 2){
            thiz.append('<div class="tick" data-n="'+ n +'"><img src="img/tick-16.png" alt="" /></div>');
            $('input[name="story'+ n +'"]').attr('value', val)
        }else{
            thiz.find('.tick').each(function () {
                $('input[name="story'+ $(this).data('n') +'"]').attr('value', '0');
                $(this).remove();
            });
            
        }
    });

    $('#first_step li').click(function () {
        $(this).siblings().removeClass('active');
        $(this).addClass('active')

        $('input[name="person"]').val($(this).data('value'))
    });

    $('.error_box').click(function () {
        $(this).fadeOut(500);
    });

})(this);

$(document).ready(function () {

    let review = $('#review').html()

    if (review === 'True') {
        $('#like').removeClass('heart-outline');
        $('#like').addClass('heart');
    }

    if (review === 'False') {
        $('#dislike').removeClass('heart-broken-outline');
        $('#dislike').addClass('heart-broken');
    }

    $('#like').click(function () {
        let remove;
        let changeReview = false;

        //change fill
        if ($(this).hasClass('heart-outline')) {
            $(this).removeClass('heart-outline');
            $(this).addClass('heart');
            remove = false;
        }else if ($(this).hasClass('heart')) {
            $(this).removeClass('heart');
            $(this).addClass('heart-outline');
            remove = true;
        }

        //change review on like
        if ($('#dislike').hasClass('heart-broken')) {
            $('#dislike').removeClass('heart-broken');
            $('#dislike').addClass('heart-broken-outline');
            changeReview = true;
        }

        $.ajax({
            data: {
                menu_id: $('#menu_id').html(),
                remove: remove,
                change: changeReview,
            },
            url: 'menu_like',

            success: function (response) {
                console.log(response);
            },
            error: function (response) {
                console.log(response.responseJSON.errors);
            },
        });
        return false;
    });


    $('#dislike').click(function () {
        let remove;
        let changeReview = false;

        //change fill
        if ($(this).hasClass('heart-broken-outline')) {
            $(this).removeClass('heart-broken-outline');
            $(this).addClass('heart-broken');
            remove = false;
        }else if ($(this).hasClass('heart-broken')) {
            $(this).removeClass('heart-broken');
            $(this).addClass('heart-broken-outline');
            remove = true;
        }

        //change review on dislike
        if ($('#like').hasClass('heart')) {
            $('#like').removeClass('heart');
            $('#like').addClass('heart-outline');
            changeReview = true;
        }

        $.ajax({
            data: {
                menu_id: $('#menu_id').html(),
                remove: remove,
                change: changeReview,
            },
            url: 'menu_dislike',

            success: function (response) {
                console.log(response);
            },
            error: function (response) {
                console.log(response.responseJSON.errors);
            },
        });
        return false;
    });
})
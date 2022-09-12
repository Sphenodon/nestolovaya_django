$(document).ready(function () {
    const blockquote = $('.blockquote');
    const review = $('#review').html();
    const user_auth = $('#user_auth').html();

    if (review === 'true') {
        $('#like').removeClass('heart-outline');
        $('#like').addClass('heart');
    }

    if (review === 'false') {
        $('#dislike').removeClass('heart-broken-outline');
        $('#dislike').addClass('heart-broken');
    }

    const check_auth = function () {
        if (user_auth === 'false') {
            $(`<p class="card-text mb-0">Для возможности оценивания требуется авторизация</p>
               <div class="">
                    <a href="/login/vk-oauth2/" class="">
                        <svg width="44" height="44" viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M6.5306 6.5306C4 9.06119 4 13.1341 4 21.28V22.72C4 30.8659 4 34.9388 6.5306 37.4694C9.0612 40 13.1341 40 21.28 40H22.72C30.8659 40 34.9388 40 37.4694 37.4694C40 34.9388 40 30.8659 40 22.72V21.28C40 13.1341 40 9.06119 37.4694 6.5306C34.9388 4 30.8659 4 22.72 4H21.28C13.1341 4 9.0612 4 6.5306 6.5306ZM10 15C10.1949 24.3694 14.8719 30 23.0718 30H23.5366V24.6396C26.5497 24.9399 28.8281 27.1471 29.7425 30H34C32.8307 25.7357 29.7575 23.3784 27.8387 22.4775C29.7575 21.3663 32.4558 18.6637 33.1004 15H29.2327C28.3932 17.973 25.9051 20.6757 23.5366 20.9309V15H19.6689V25.3904C17.2704 24.7898 14.2423 21.8769 14.1074 15H10Z" fill="currentColor"></path>
                        </svg>
                    </a>
               </div>`).appendTo(blockquote);
            $('.container-review').remove();
            return false;
        }
    }

    $('#like').click(function () {
        if (check_auth() === false) return;

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

        //change review if was dislike
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
        if (check_auth() === false) return;

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
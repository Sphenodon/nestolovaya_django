$(document).ready(function () {
    //for categories (anchor)
    $(".scroll-to").on("click", function () {
        let anchor = $(this).html();
        let scrollTopHeight;

        if ($('.categories').hasClass('is-fixed')) {
            scrollTopHeight = $(`#${anchor.replace(/\s+/g, '')}`).offset().top - $('.categories__wrap').height() - 15;
        } else scrollTopHeight = $(`#${anchor.replace(/\s+/g, '')}`).offset().top - $('.categories__wrap').height() - 95;

        $('html, body').animate(
            {scrollTop: scrollTopHeight},
            50);
    });

    //for categories__wrap
    $(document).on("scroll", function () {
        let positionY = $(document).scrollTop();
        if (positionY >= 130) {
            $('.categories').addClass('is-fixed');
        }
        if (positionY < 130) {
            $('.categories').removeClass('is-fixed');
        }
    });

    //for button in slider
    let sumWidth = 0;
    $('.categories__item').each(function () {
        if ($(this).width()) {
            sumWidth += $(this).width();
        }
    })
    if ($('.carousel-slider__container').width() > sumWidth) {
        $('.categories-toggle-button__wrapper').css('display', 'none');
        $('.carousel-slider__container').css('white-space', 'normal')
    }

    //for button carousel-slider__container
    const carouselSliderContainer = $('.carousel-slider__container');
    $(document).on("click", '.categories-toggle-button', function () {
        if (carouselSliderContainer.css('white-space') === 'nowrap') {
            carouselSliderContainer.css('white-space', 'normal');
        } else if ($('.carousel-slider__container').css('white-space') === 'normal') {
            carouselSliderContainer.css('white-space', 'nowrap');
        }
    });

});
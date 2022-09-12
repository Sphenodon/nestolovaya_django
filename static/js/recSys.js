const emotionWeight = 1;
const finalCoefficientWeight = 0.15;
let menuByEm;
let arrForDrinks = [];
let arrForFood = [];
let arrForDessert = [];
let arrForCombo = [];
let imagesForDrinks = [];
let imagesForFood = [];
let imagesForDessert = [];
let imagesForCombo = [];
let emotion;

$(document).ready(function () {
    //clear data in slots
    $('#btn-choose').click(function () {
        $($('.slot')[0]).html('');
        $($('.slot')[1]).html('');
        $($('.slot')[2]).html('');
    });

    $('.smile').click(function () {
        //check emotion
        // if (emotion === $(this).attr('id')) return;
        $.ajax({
            data: {emotion: $(this).attr('id')},
            url: 'menu_by_em',

            success: function (response) {
                emotion = response.menu_by_em[0].emotioncoefficient__emotion;
                menuByEm = response.menu_by_em;
                console.log(menuByEm);
                dataProcedures();
                if ( ! $('.container-slot-spin').html()){
                    $('.container-slot-footer').remove()
                }
                runSlots();
            },
            error: function (response) {
                console.log(response.responseJSON.errors);
            },
        });
        return false;
    });

    $(document).on("click", '.button-review-recommendation', function () {
        let currentImages = [
            $('#slot1 img').attr('src').slice(48),
            $('#slot2 img').attr('src').slice(48),
            $('#slot3 img').attr('src').slice(48)
        ]
        let review = $(this).attr('id')
        console.log(currentImages)
        console.log(review)

        $.ajax({
            data: {
                images: currentImages,
                emotion: emotion,
                review: review
            },
            url: 'menu_review_recommendation',

            success: function (response) {
                console.log(response)
                continueRecommendation();
            },
            error: function (response) {
                console.log(response.responseJSON.errors);
            },
        });
        return false;
    });

    $(document).on("click", '.container-slot-footer-close-review', function () {
        let currentImages = [
            $('#slot1 img').attr('src').slice(7),
            $('#slot2 img').attr('src').slice(7),
            $('#slot3 img').attr('src').slice(7)
        ]

        console.log(currentImages)

        $.ajax({
            data: {
                images: currentImages,
                emotion: emotion,
                review: 'indifferent'
            },
            url: 'menu_review_recommendation',

            success: function (response) {
                console.log(response)
                continueRecommendation();
            },
            error: function (response) {
                console.log(response.responseJSON.errors);
            },
        });
        return false;
    });

    function continueRecommendation(){
        if (imagesForDrinks.length && imagesForFood.length && imagesForDessert.length){
            $('.container-slot-footer').remove();
            $('.container-slot').append('<div class="container-slot-spin">\n' +
                        '                            <button class="container-slot-spin-button">\n' +
                        '                                Подобрать\n' +
                        '                            </button>\n' +
                        '                        </div>')
        }else {
            $('.container-slot-footer-info').html('Предложения кончились');
            $('.container-slot-footer-review').remove();
            $('.container-slot-footer-close-review').remove();
        }
    }

    function dataProcedures(){
        arrForDrinks = [];
        arrForFood = [];
        arrForDessert = [];
        arrForCombo = [];
        imagesForDrinks = [];
        imagesForFood = [];
        imagesForDessert = [];
        imagesForCombo = [];

        menuByEm.sort( function (a,b){
            return b.emotioncoefficient__coefficient - a.emotioncoefficient__coefficient;
        })

        let max_emotion_coefficient = menuByEm[0].emotioncoefficient__coefficient
        if (max_emotion_coefficient === 0 || max_emotion_coefficient < 0) max_emotion_coefficient = 1;

        console.log(`max_emotion_coefficient: ${max_emotion_coefficient}`)

        for (let i of menuByEm){
            if (i.food_type === 'DR') {
                i.finalCoefWithEmotion = finalCoefficientWeight*i.final_coefficient + emotionWeight * i.emotioncoefficient__coefficient / max_emotion_coefficient * 100;
                arrForDrinks.push(i);
            }
            if (i.food_type === 'FO') {
                i.finalCoefWithEmotion = finalCoefficientWeight*i.final_coefficient + emotionWeight * i.emotioncoefficient__coefficient / max_emotion_coefficient * 100;
                arrForFood.push(i);
            }
            if (i.food_type === 'DE') {
                i.finalCoefWithEmotion = finalCoefficientWeight*i.final_coefficient + emotionWeight * i.emotioncoefficient__coefficient / max_emotion_coefficient * 100;
                arrForDessert.push(i);
            }
            if (i.food_type === 'CO') {
                i.finalCoefWithEmotion = finalCoefficientWeight*i.final_coefficient + emotionWeight * i.emotioncoefficient__coefficient / max_emotion_coefficient * 100;
                arrForCombo.push(i);
            }
        }

        arrForDrinks.sort(function (a, b){
            return a.finalCoefWithEmotion - b.finalCoefWithEmotion;
        })
        arrForFood.sort(function (a, b){
            return a.finalCoefWithEmotion - b.finalCoefWithEmotion;
        })
        arrForDessert.sort(function (a, b){
            return a.finalCoefWithEmotion - b.finalCoefWithEmotion;
        })
        arrForCombo.sort(function (a, b){
            return a.finalCoefWithEmotion - b.finalCoefWithEmotion;
        })

        for (let i of arrForDrinks){
            imagesForDrinks.push({'image': i.image, 'menu_id': i.id, 'coefWithEmotion': i.finalCoefWithEmotion});
        }
        for (let i of arrForFood){
            imagesForFood.push({'image': i.image, 'menu_id': i.id, 'coefWithEmotion': i.finalCoefWithEmotion});
        }
        for (let i of arrForDessert){
            imagesForDessert.push({'image': i.image, 'menu_id': i.id, 'coefWithEmotion': i.finalCoefWithEmotion});
        }
        for (let i of arrForCombo){
            imagesForCombo.push({'image': i.image, 'menu_id': i.id, 'coefWithEmotion': i.finalCoefWithEmotion});
        }

        console.log(imagesForDrinks)
    }

    function runSlots() {

        let imageBatchForDrinks = imagesForDrinks.pop();
        let imageBatchForFood = imagesForFood.pop();
        let imageBatchForDessert = imagesForDessert.pop();

        let slot1 = $('#slot1');
        let slot2 = $('#slot2');
        let slot3 = $('#slot3');

        try {
            slot1.html(`<img src = "https://storage.yandexcloud.net/for-nestolovaya/${imageBatchForDrinks.image}">`);
            slot1.append(`<a class="stretched-link" href="/menu/detail/${imageBatchForDrinks.menu_id}/"></a>`);
        }catch (e){
            /* images ran out */
        }
        try {
            slot2.html(`<img src = "https://storage.yandexcloud.net/for-nestolovaya/${imageBatchForFood.image}">`);
            slot2.append(`<a class="stretched-link" href="/menu/detail/${imageBatchForFood.menu_id}/"></a>`);
        }catch (e){
            /* images ran out */
        }
        try {
            slot3.html(`<img src = "https://storage.yandexcloud.net/for-nestolovaya/${imageBatchForDessert.image}">`);
            slot3.append(`<a class="stretched-link" href="/menu/detail/${imageBatchForDessert.menu_id}/"></a>`);
        }catch (e){
            /* images ran out */
        }

        $('.container-slot-spin').remove();
        $('.container-slot').append(
            `<div class="container-slot-footer">
                <div class="container-slot-footer-header">
                    <span class="container-slot-footer-info">Понравилось предложение?</span>
                </div>
                <div class="container-slot-footer-review">
                    <svg class="button-review-recommendation" xmlns="http://www.w3.org/2000/svg"
                         viewBox="0 0 28 28" id="correct">
                        <path d="M18.77,11h-4.23l1.52-4.94C16.38,5.03,15.54,4,14.38,4c-0.58,0-1.14,0.24-1.52,0.65L7,11H3v10h4h1h9.43 c1.06,0,1.98-0.67,2.19-1.61l1.34-6C21.23,12.15,20.18,11,18.77,11z M7,20H4v-8h3V20z M19.98,13.17l-1.34,6 C18.54,19.65,18.03,20,17.43,20H8v-8.61l5.6-6.06C13.79,5.12,14.08,5,14.38,5c0.26,0,0.5,0.11,0.63,0.3 c0.07,0.1,0.15,0.26,0.09,0.47l-1.52,4.94L13.18,12h1.35h4.23c0.41,0,0.8,0.17,1.03,0.46C19.92,12.61,20.05,12.86,19.98,13.17z"></path>
                    </svg>
                    <svg class="button-review-recommendation" xmlns="http://www.w3.org/2000/svg"
                         viewBox="0 0 28 28" id="wrong">
                        <path d="M17,4h-1H6.57C5.5,4,4.59,4.67,4.38,5.61l-1.34,6C2.77,12.85,3.82,14,5.23,14h4.23l-1.52,4.94C7.62,19.97,8.46,21,9.62,21 c0.58,0,1.14-0.24,1.52-0.65L17,14h4V4H17z M10.4,19.67C10.21,19.88,9.92,20,9.62,20c-0.26,0-0.5-0.11-0.63-0.3 c-0.07-0.1-0.15-0.26-0.09-0.47l1.52-4.94l0.4-1.29H9.46H5.23c-0.41,0-0.8-0.17-1.03-0.46c-0.12-0.15-0.25-0.4-0.18-0.72l1.34-6 C5.46,5.35,5.97,5,6.57,5H16v8.61L10.4,19.67z M20,13h-3V5h3V13z"></path>
                    </svg>
                </div>
                
                <button class="container-slot-footer-close-review">
                    Подобрать ещё
                </button>
            </div>`);
    }


    $(document).on("click", '.container-slot-spin-button', function () {
        runSlots();
    });
});